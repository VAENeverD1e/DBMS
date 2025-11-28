"""app.utils.common
Reusable utilities for the backend.

This module provides a central logging helper so any backend file
can import and call `log`, `info`, `warning`, `error`, or `debug`.

Usage examples:
	from app.utils.common import info, error

	info('User created', extra={'user_id': user_id})

The logger will automatically include basic Flask request context
if called within an application/request context.
"""
from __future__ import annotations

import logging
import logging.handlers
import os
import traceback
from typing import Any, Dict, Optional

try:
	# Flask context imports are optional so this module can be used in scripts
	from flask import current_app, has_request_context, request
except Exception:
	current_app = None  # type: ignore
	has_request_context = lambda: False  # type: ignore
	request = None  # type: ignore


# Module-level logger configuration guard
_LOGGER_CONFIGURED = False


def _configure_logger():
	"""Configure the root logger once.

	Reads optional configuration from Flask `current_app.config` when available:
	  - LOG_LEVEL: 'DEBUG'|'INFO'|... (default: INFO)
	  - LOG_TO_FILE: bool (default: False)
	  - LOG_FILE_PATH: path (default: 'logs/backend.log')
	"""
	global _LOGGER_CONFIGURED
	if _LOGGER_CONFIGURED:
		return

	level_name = 'INFO'
	log_to_file = False
	log_file_path = os.path.join('logs', 'backend.log')

	try:
		if current_app:
			cfg = current_app.config
			level_name = cfg.get('LOG_LEVEL', level_name)
			log_to_file = cfg.get('LOG_TO_FILE', log_to_file)
			log_file_path = cfg.get('LOG_FILE_PATH', log_file_path)
	except Exception:
		# If no Flask app context, fall back to environment and defaults
		level_name = os.environ.get('LOG_LEVEL', level_name)
		log_to_file = os.environ.get('LOG_TO_FILE', 'False') in ('True', 'true', '1')
		log_file_path = os.environ.get('LOG_FILE_PATH', log_file_path)

	level = getattr(logging, level_name.upper(), logging.INFO)

	root = logging.getLogger()
	root.setLevel(level)

	# Console handler
	ch = logging.StreamHandler()
	ch.setLevel(level)
	fmt = '%(asctime)s %(levelname)s %(name)s: %(message)s'
	ch.setFormatter(logging.Formatter(fmt))
	root.addHandler(ch)

	# Optional rotating file handler
	if log_to_file:
		os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
		fh = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3)
		fh.setLevel(level)
		fh.setFormatter(logging.Formatter(fmt))
		root.addHandler(fh)

	_LOGGER_CONFIGURED = True


def _enrich_message(message: str, extra: Optional[Dict[str, Any]] = None) -> str:
	parts = [message]
	try:
		if has_request_context():
			# Add simple request context for easier debugging
			parts.append(f"path={request.path}")
			parts.append(f"method={request.method}")
			if request.remote_addr:
				parts.append(f"remote_addr={request.remote_addr}")
			# If user info is provided in headers (e.g. Authorization), keep it short
			user = request.headers.get('X-User-Id') or request.headers.get('X-User')
			if user:
				parts.append(f"user={user}")
	except Exception:
		# silently ignore enrichment errors
		parts.append('context_error')

	if extra:
		try:
			parts.append('extra=' + str(extra))
		except Exception:
			parts.append('extra=<unserializable>')

	return ' | '.join(parts)


def log(message: str, level: str = 'info', extra: Optional[Dict[str, Any]] = None, exc: Optional[BaseException] = None) -> None:
	"""Generic logging helper.

	Args:
		message: main message to log
		level: one of 'debug','info','warning','error','critical'
		extra: optional dict to include in the message
		exc: optional exception instance — its traceback will be logged
	"""
	_configure_logger()
	msg = _enrich_message(message, extra)
	logger = logging.getLogger('backend')
	level = (level or 'info').lower()
	try:
		if level == 'debug':
			logger.debug(msg)
		elif level == 'warning':
			logger.warning(msg)
		elif level == 'error':
			if exc:
				logger.error(msg + '\n' + ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
			else:
				logger.error(msg)
		elif level == 'critical':
			logger.critical(msg)
		else:
			logger.info(msg)
	except Exception:
		# As a last resort use print to avoid raising from logger
		try:
			print(msg)
			if exc:
				print(''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
		except Exception:
			pass


def info(message: str, extra: Optional[Dict[str, Any]] = None) -> None:
	log(message, 'info', extra)


def debug(message: str, extra: Optional[Dict[str, Any]] = None) -> None:
	log(message, 'debug', extra)


def warning(message: str, extra: Optional[Dict[str, Any]] = None) -> None:
	log(message, 'warning', extra)


def error(message: str, extra: Optional[Dict[str, Any]] = None, exc: Optional[BaseException] = None) -> None:
	log(message, 'error', extra, exc)


def critical(message: str, extra: Optional[Dict[str, Any]] = None) -> None:
	log(message, 'critical', extra)

