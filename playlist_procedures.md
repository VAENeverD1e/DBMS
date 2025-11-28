# Playlist Stored Procedures & Constraints

Tài liệu này mô tả các thủ tục (stored procedure) thao tác với bảng `Playlist` và bảng liên kết bài hát trong playlist (ví dụ `Contain` hoặc `PlaylistSong`) sao cho phù hợp với hệ thống hiện tại **và** hai semantic constraint sau:

- **Playlist Song Limit**: Một Playlist chứa tối đa **360** bài hát.
- **Playlist Ownership**: Một Listener **không được tạo hai Playlist trùng tên**.

Giả sử lược đồ chính như sau (tên bảng/cột khớp với code backend hiện tại):

```sql
-- Bảng Listener
-- Listener(ListenerID PK, UserID FK ...)

-- Bảng Playlist
-- Playlist(
--   PlaylistID INT AUTO_INCREMENT PRIMARY KEY,
--   ListenerID INT NOT NULL,
--   Name       VARCHAR(255) NOT NULL,
--   CreateDate DATETIME DEFAULT CURRENT_TIMESTAMP,
--   ...,
--   CONSTRAINT fk_playlist_listener
--     FOREIGN KEY (ListenerID) REFERENCES Listener(ListenerID)
-- ) ENGINE=InnoDB;

-- Bảng liên kết bài hát trong playlist (trùng với backend: Contain)
-- Contain(
--   PlaylistID INT NOT NULL,
--   SingleID   INT NOT NULL,
--   PRIMARY KEY (PlaylistID, SingleID),
--   FOREIGN KEY (PlaylistID) REFERENCES Playlist(PlaylistID)
--     ON DELETE CASCADE,
--   FOREIGN KEY (SingleID)   REFERENCES Single(SingleID)
-- );
```

---

## 1. Ràng buộc sở hữu playlist (Playlist Ownership)

### 1.1. Unique index theo Listener + Name

Để đảm bảo **một Listener không thể có hai Playlist cùng tên**, tạo unique index như sau:

```sql
ALTER TABLE Playlist
ADD CONSTRAINT uq_listener_playlist_name
UNIQUE (ListenerID, Name);
```

Với unique này, mọi thao tác INSERT/UPDATE vi phạm sẽ bị MySQL báo lỗi (error code 1062). Trong stored procedure ta sẽ **chủ động kiểm tra trước** để trả về thông điệp lỗi rõ ràng.

---

## 2. Thủ tục tạo playlist (INSERT)

Ràng buộc:
- Phải là Listener hợp lệ.
- Tên playlist không rỗng, độ dài <= 255.
- Listener **chưa có playlist nào trùng tên**.

```sql
DELIMITER $$

CREATE PROCEDURE sp_create_playlist (
    IN  p_user_id    INT,
    IN  p_name       VARCHAR(255),
    OUT p_success    TINYINT,
    OUT p_message    VARCHAR(255),
    OUT p_playlist_id INT
)
BEGIN
    DECLARE v_listener_id INT;
    DECLARE v_count INT;

    SET p_success = 0;
    SET p_message = '';
    SET p_playlist_id = NULL;

    -- 1. Kiểm tra tên hợp lệ
    IF p_name IS NULL OR CHAR_LENGTH(TRIM(p_name)) = 0 THEN
        SET p_message = 'Playlist name cannot be empty';
        LEAVE proc_end;
    END IF;

    IF CHAR_LENGTH(p_name) > 255 THEN
        SET p_message = 'Playlist name must not exceed 255 characters';
        LEAVE proc_end;
    END IF;

    -- 2. Lấy ListenerID từ UserID
    SELECT ListenerID INTO v_listener_id
    FROM Listener
    WHERE UserID = p_user_id
    LIMIT 1;

    IF v_listener_id IS NULL THEN
        SET p_message = 'User is not a listener';
        LEAVE proc_end;
    END IF;

    -- 3. Kiểm tra xem listener đã có playlist trùng tên chưa
    SELECT COUNT(*) INTO v_count
    FROM Playlist
    WHERE ListenerID = v_listener_id
      AND Name = p_name;

    IF v_count > 0 THEN
        SET p_message = 'You already have a playlist with this name';
        LEAVE proc_end;
    END IF;

    -- 4. Thêm playlist
    INSERT INTO Playlist (ListenerID, Name)
    VALUES (v_listener_id, p_name);

    SET p_playlist_id = LAST_INSERT_ID();
    SET p_success = 1;
    SET p_message = 'Playlist created successfully';

proc_end:
    -- exit label
    BEGIN END;
END $$

DELIMITER ;
```

> Ghi chú: backend hiện tại đang chạy query thuần, không gọi procedure. Bạn có thể gọi `sp_create_playlist` từ client SQL hoặc sửa backend để dùng procedure này nếu muốn.

---

## 3. Thủ tục sửa tên playlist (UPDATE)

Ràng buộc:
- User phải là Listener hợp lệ.
- Playlist phải tồn tại.
- User phải là **chủ sở hữu** playlist.
- Tên mới không rỗng, <= 255.
- Tên mới **không trùng** với playlist khác của cùng Listener.

```sql
DELIMITER $$

CREATE PROCEDURE sp_update_playlist_name (
    IN  p_user_id     INT,
    IN  p_playlist_id INT,
    IN  p_new_name    VARCHAR(255),
    OUT p_success     TINYINT,
    OUT p_message     VARCHAR(255)
)
BEGIN
    DECLARE v_listener_id INT;
    DECLARE v_owner_listener_id INT;
    DECLARE v_count INT;

    SET p_success = 0;
    SET p_message = '';

    -- 1. Validate tên
    IF p_new_name IS NULL OR CHAR_LENGTH(TRIM(p_new_name)) = 0 THEN
        SET p_message = 'Playlist name cannot be empty';
        LEAVE proc_end;
    END IF;

    IF CHAR_LENGTH(p_new_name) > 255 THEN
        SET p_message = 'Playlist name must not exceed 255 characters';
        LEAVE proc_end;
    END IF;

    -- 2. Lấy ListenerID từ UserID
    SELECT ListenerID INTO v_listener_id
    FROM Listener
    WHERE UserID = p_user_id
    LIMIT 1;

    IF v_listener_id IS NULL THEN
        SET p_message = 'User is not a listener';
        LEAVE proc_end;
    END IF;

    -- 3. Kiểm tra playlist tồn tại + lấy owner
    SELECT ListenerID INTO v_owner_listener_id
    FROM Playlist
    WHERE PlaylistID = p_playlist_id
    LIMIT 1;

    IF v_owner_listener_id IS NULL THEN
        SET p_message = 'Playlist not found';
        LEAVE proc_end;
    END IF;

    -- 4. Kiểm tra quyền sở hữu
    IF v_owner_listener_id <> v_listener_id THEN
        SET p_message = 'You are not the owner of this playlist';
        LEAVE proc_end;
    END IF;

    -- 5. Kiểm tra trùng tên với playlist khác của cùng listener
    SELECT COUNT(*) INTO v_count
    FROM Playlist
    WHERE ListenerID = v_listener_id
      AND Name = p_new_name
      AND PlaylistID <> p_playlist_id;

    IF v_count > 0 THEN
        SET p_message = 'You already have another playlist with this name';
        LEAVE proc_end;
    END IF;

    -- 6. Cập nhật tên
    UPDATE Playlist
    SET Name = p_new_name
    WHERE PlaylistID = p_playlist_id;

    SET p_success = 1;
    SET p_message = 'Playlist updated successfully';

proc_end:
    BEGIN END;
END $$

DELIMITER ;
```

---

## 4. Thủ tục xóa playlist (DELETE)

Ràng buộc:
- User là Listener.
- Playlist tồn tại.
- Listener hiện tại là chủ sở hữu.
- Khi xóa playlist, các bản ghi trong `Contain` sẽ được xóa nhờ `ON DELETE CASCADE`.

```sql
DELIMITER $$

CREATE PROCEDURE sp_delete_playlist (
    IN  p_user_id     INT,
    IN  p_playlist_id INT,
    OUT p_success     TINYINT,
    OUT p_message     VARCHAR(255)
)
BEGIN
    DECLARE v_listener_id INT;
    DECLARE v_owner_listener_id INT;

    SET p_success = 0;
    SET p_message = '';

    -- 1. Lấy ListenerID từ UserID
    SELECT ListenerID INTO v_listener_id
    FROM Listener
    WHERE UserID = p_user_id
    LIMIT 1;

    IF v_listener_id IS NULL THEN
        SET p_message = 'User is not a listener';
        LEAVE proc_end;
    END IF;

    -- 2. Kiểm tra playlist tồn tại & owner
    SELECT ListenerID INTO v_owner_listener_id
    FROM Playlist
    WHERE PlaylistID = p_playlist_id
    LIMIT 1;

    IF v_owner_listener_id IS NULL THEN
        SET p_message = 'Playlist not found';
        LEAVE proc_end;
    END IF;

    IF v_owner_listener_id <> v_listener_id THEN
        SET p_message = 'You are not the owner of this playlist';
        LEAVE proc_end;
    END IF;

    -- 3. Xóa playlist (Contain sẽ bị xóa nhờ ON DELETE CASCADE)
    DELETE FROM Playlist
    WHERE PlaylistID = p_playlist_id;

    SET p_success = 1;
    SET p_message = 'Playlist deleted successfully';

proc_end:
    BEGIN END;
END $$

DELIMITER ;
```

---

## 5. Thủ tục thêm bài hát vào playlist (INSERT vào Contain) với giới hạn 360 bài

Ràng buộc:
- User là Listener.
- Playlist tồn tại & thuộc về listener đó.
- Bài hát (Single) tồn tại.
- Bài hát chưa có trong playlist.
- Playlist **không vượt quá 360 bài**.

```sql
DELIMITER $$

CREATE PROCEDURE sp_add_song_to_playlist (
    IN  p_user_id     INT,
    IN  p_playlist_id INT,
    IN  p_song_id     INT,
    OUT p_success     TINYINT,
    OUT p_message     VARCHAR(255)
)
BEGIN
    DECLARE v_listener_id INT;
    DECLARE v_owner_listener_id INT;
    DECLARE v_song_exists INT;
    DECLARE v_already_in INT;
    DECLARE v_song_count INT;

    SET p_success = 0;
    SET p_message = '';

    -- 1. Lấy ListenerID từ UserID
    SELECT ListenerID INTO v_listener_id
    FROM Listener
    WHERE UserID = p_user_id
    LIMIT 1;

    IF v_listener_id IS NULL THEN
        SET p_message = 'User is not a listener';
        LEAVE proc_end;
    END IF;

    -- 2. Kiểm tra playlist tồn tại & owner
    SELECT ListenerID INTO v_owner_listener_id
    FROM Playlist
    WHERE PlaylistID = p_playlist_id
    LIMIT 1;

    IF v_owner_listener_id IS NULL THEN
        SET p_message = 'Playlist not found';
        LEAVE proc_end;
    END IF;

    IF v_owner_listener_id <> v_listener_id THEN
        SET p_message = 'You are not the owner of this playlist';
        LEAVE proc_end;
    END IF;

    -- 3. Kiểm tra bài hát tồn tại
    SELECT COUNT(*) INTO v_song_exists
    FROM Single
    WHERE SingleID = p_song_id;

    IF v_song_exists = 0 THEN
        SET p_message = 'Song not found';
        LEAVE proc_end;
    END IF;

    -- 4. Kiểm tra bài hát đã nằm trong playlist chưa
    SELECT COUNT(*) INTO v_already_in
    FROM Contain
    WHERE PlaylistID = p_playlist_id
      AND SingleID = p_song_id;

    IF v_already_in > 0 THEN
        SET p_message = 'Song is already in this playlist';
        LEAVE proc_end;
    END IF;

    -- 5. Đếm số lượng bài hát hiện có trong playlist
    SELECT COUNT(*) INTO v_song_count
    FROM Contain
    WHERE PlaylistID = p_playlist_id;

    IF v_song_count >= 360 THEN
        SET p_message = 'Playlist has reached the maximum limit of 360 songs';
        LEAVE proc_end;
    END IF;

    -- 6. Thêm bài hát vào playlist
    INSERT INTO Contain (PlaylistID, SingleID)
    VALUES (p_playlist_id, p_song_id);

    SET p_success = 1;
    SET p_message = 'Song added to playlist successfully';

proc_end:
    BEGIN END;
END $$

DELIMITER ;
```

---

## 6. Thủ tục xóa bài hát khỏi playlist (DELETE từ Contain)

Ràng buộc:
- User là Listener.
- Playlist tồn tại & thuộc về listener.
- Bài hát đang nằm trong playlist.

```sql
DELIMITER $$

CREATE PROCEDURE sp_remove_song_from_playlist (
    IN  p_user_id     INT,
    IN  p_playlist_id INT,
    IN  p_song_id     INT,
    OUT p_success     TINYINT,
    OUT p_message     VARCHAR(255)
)
BEGIN
    DECLARE v_listener_id INT;
    DECLARE v_owner_listener_id INT;
    DECLARE v_in_playlist INT;

    SET p_success = 0;
    SET p_message = '';

    -- 1. Lấy ListenerID từ UserID
    SELECT ListenerID INTO v_listener_id
    FROM Listener
    WHERE UserID = p_user_id
    LIMIT 1;

    IF v_listener_id IS NULL THEN
        SET p_message = 'User is not a listener';
        LEAVE proc_end;
    END IF;

    -- 2. Kiểm tra playlist tồn tại & owner
    SELECT ListenerID INTO v_owner_listener_id
    FROM Playlist
    WHERE PlaylistID = p_playlist_id
    LIMIT 1;

    IF v_owner_listener_id IS NULL THEN
        SET p_message = 'Playlist not found';
        LEAVE proc_end;
    END IF;

    IF v_owner_listener_id <> v_listener_id THEN
        SET p_message = 'You are not the owner of this playlist';
        LEAVE proc_end;
    END IF;

    -- 3. Kiểm tra bài hát có trong playlist không
    SELECT COUNT(*) INTO v_in_playlist
    FROM Contain
    WHERE PlaylistID = p_playlist_id
      AND SingleID = p_song_id;

    IF v_in_playlist = 0 THEN
        SET p_message = 'Song is not in this playlist';
        LEAVE proc_end;
    END IF;

    -- 4. Xóa bài hát khỏi playlist
    DELETE FROM Contain
    WHERE PlaylistID = p_playlist_id
      AND SingleID = p_song_id;

    SET p_success = 1;
    SET p_message = 'Song removed from playlist successfully';

proc_end:
    BEGIN END;
END $$

DELIMITER ;
```

---

## 7. Cách sử dụng với database của bạn

Ví dụ gọi trên MySQL:

```sql
-- Tạo playlist mới
CALL sp_create_playlist(1, 'My Playlist', @ok, @msg, @new_id);
SELECT @ok AS success, @msg AS message, @new_id AS playlist_id;

-- Đổi tên playlist
CALL sp_update_playlist_name(1, @new_id, 'My Renamed Playlist', @ok, @msg);
SELECT @ok, @msg;

-- Thêm bài hát vào playlist
CALL sp_add_song_to_playlist(1, @new_id, 123, @ok, @msg);
SELECT @ok, @msg;

-- Xóa bài hát khỏi playlist
CALL sp_remove_song_from_playlist(1, @new_id, 123, @ok, @msg);
SELECT @ok, @msg;

-- Xóa playlist
CALL sp_delete_playlist(1, @new_id, @ok, @msg);
SELECT @ok, @msg;
```

Bạn có thể copy toàn bộ script trong file này, chạy trên MySQL Workbench / phpMyAdmin để tạo các procedure, sau đó dùng trực tiếp để tương tác với database hoặc chỉnh backend để gọi thay vì dùng câu lệnh SQL thuần.
