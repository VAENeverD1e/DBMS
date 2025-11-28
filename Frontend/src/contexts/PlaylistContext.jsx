import React, { createContext, useReducer, useCallback, useContext } from 'react';
import playlistService from '../services/playlistService';

const PlaylistContext = createContext();

const initialState = {
  playlists: [],
  loading: false,
  error: null,
  totalCount: 0,
};

const playlistReducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload, error: null };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    case 'SET_PLAYLISTS':
      return {
        ...state,
        playlists: action.payload.playlists,
        totalCount: action.payload.total_count,
        loading: false,
        error: null,
      };
    case 'ADD_PLAYLIST':
      return {
        ...state,
        playlists: [action.payload, ...state.playlists],
        totalCount: state.totalCount + 1,
      };
    case 'UPDATE_PLAYLIST':
      return {
        ...state,
        playlists: state.playlists.map((p) =>
          p.playlist_id === action.payload.playlist_id ? action.payload : p
        ),
      };
    case 'DELETE_PLAYLIST':
      return {
        ...state,
        playlists: state.playlists.filter(
          (p) => p.playlist_id !== action.payload
        ),
        totalCount: state.totalCount - 1,
      };
    case 'UPDATE_SONG_COUNT':
      return {
        ...state,
        playlists: state.playlists.map((p) =>
          p.playlist_id === action.payload.playlistId
            ? { ...p, song_count: action.payload.newCount }
            : p
        ),
      };
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    default:
      return state;
  }
};

export const PlaylistProvider = ({ children }) => {
  const [state, dispatch] = useReducer(playlistReducer, initialState);

  const fetchPlaylists = useCallback(async (limit = 50, offset = 0) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    const result = await playlistService.getUserPlaylists(limit, offset);
    
    if (result.success) {
      dispatch({
        type: 'SET_PLAYLISTS',
        payload: {
          playlists: result.playlists,
          total_count: result.total_count,
        },
      });
    } else {
      dispatch({ type: 'SET_ERROR', payload: result.error || 'Failed to fetch playlists' });
    }
  }, []);

  const createPlaylist = useCallback(async (name) => {
    dispatch({ type: 'SET_LOADING', payload: true });
    const result = await playlistService.createPlaylist(name);
    
    if (result.success) {
      dispatch({ type: 'ADD_PLAYLIST', payload: result.playlist });
      return { success: true, playlist: result.playlist };
    } else {
      dispatch({ type: 'SET_ERROR', payload: result.error || 'Failed to create playlist' });
      return { success: false, error: result.error };
    }
  }, []);

  const deletePlaylist = useCallback(async (playlistId) => {
    const result = await playlistService.deletePlaylist(playlistId);
    
    if (result.success) {
      dispatch({ type: 'DELETE_PLAYLIST', payload: playlistId });
      return { success: true };
    } else {
      dispatch({ type: 'SET_ERROR', payload: result.error || 'Failed to delete playlist' });
      return { success: false, error: result.error };
    }
  }, []);

  const updatePlaylist = useCallback(async (playlistId, name) => {
    const result = await playlistService.updatePlaylist(playlistId, name);
    
    if (result.success) {
      // Optionally refresh to get updated data
      return { success: true };
    } else {
      dispatch({ type: 'SET_ERROR', payload: result.error || 'Failed to update playlist' });
      return { success: false, error: result.error };
    }
  }, []);

  const addSongToPlaylist = useCallback(async (playlistId, songId) => {
    const result = await playlistService.addSongToPlaylist(playlistId, songId);
    
    if (result.success) {
      // Update song count in state
      dispatch({
        type: 'UPDATE_SONG_COUNT',
        payload: {
          playlistId,
          newCount: (
            state.playlists.find((p) => p.playlist_id === playlistId)?.song_count || 0
          ) + 1,
        },
      });
      return { success: true };
    } else {
      // Check if it's a duplicate song error (409)
      if (result.status === 409) {
        return { success: false, error: 'Song is already in this playlist', isDuplicate: true };
      }
      return { success: false, error: result.error };
    }
  }, [state.playlists]);

  const removeSongFromPlaylist = useCallback(async (playlistId, songId) => {
    const result = await playlistService.removeSongFromPlaylist(playlistId, songId);
    
    if (result.success) {
      // Update song count in state
      dispatch({
        type: 'UPDATE_SONG_COUNT',
        payload: {
          playlistId,
          newCount: Math.max(
            0,
            (state.playlists.find((p) => p.playlist_id === playlistId)?.song_count || 1) - 1
          ),
        },
      });
      return { success: true };
    } else {
      return { success: false, error: result.error };
    }
  }, [state.playlists]);

  const clearError = useCallback(() => {
    dispatch({ type: 'CLEAR_ERROR' });
  }, []);

  const value = {
    // State
    playlists: state.playlists,
    loading: state.loading,
    error: state.error,
    totalCount: state.totalCount,
    
    // Actions
    fetchPlaylists,
    createPlaylist,
    deletePlaylist,
    updatePlaylist,
    addSongToPlaylist,
    removeSongFromPlaylist,
    clearError,
  };

  return (
    <PlaylistContext.Provider value={value}>
      {children}
    </PlaylistContext.Provider>
  );
};

/**
 * Hook to use playlist context
 * @throws {Error} if used outside PlaylistProvider
 */
export const usePlaylist = () => {
  const context = useContext(PlaylistContext);
  if (!context) {
    throw new Error('usePlaylist must be used within PlaylistProvider');
  }
  return context;
};

export default PlaylistContext;
