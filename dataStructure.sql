-- =========================
-- 1. Label
-- =========================
CREATE TABLE Label (
    LabelID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    ContactEmail VARCHAR(255),
    Country VARCHAR(100),
    FoundedYear INT
);

-- =========================
-- 2. User
-- =========================
CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL COMMENT 'Hashed password',
    Username VARCHAR(100) NOT NULL UNIQUE,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Role ENUM('Listener', 'Artist', 'Guest') NOT NULL DEFAULT 'Guest'
);
-- =========================
-- 3. Subscription
-- =========================
CREATE TABLE Subscription (
  SubscriptionID INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(100) NOT NULL,
  Price DECIMAL(10, 2) NOT NULL,
  Duration INT NOT NULL, -- e.g., in days
  Type VARCHAR(50)
);

-- =========================
-- 4. Orders
-- =========================
CREATE TABLE Orders (
  OrderID INT AUTO_INCREMENT PRIMARY KEY,
  UserID INT NOT NULL,
  SubscriptionID INT NOT NULL,
  OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE RESTRICT,
  FOREIGN KEY (SubscriptionID) REFERENCES Subscription(SubscriptionID) ON DELETE RESTRICT
);

-- =========================
-- 5. Payment
-- =========================
CREATE TABLE Payment (
  PaymentID INT AUTO_INCREMENT PRIMARY KEY,
  OrderID INT NOT NULL,
  Method VARCHAR(50),
  PaymentDate DATETIME DEFAULT CURRENT_TIMESTAMP,
  Status VARCHAR(50) DEFAULT 'Pending',
  Amount DECIMAL(10, 2) NOT NULL,
  FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE RESTRICT
);

-- =========================
-- 6. UserSubscription
-- =========================
CREATE TABLE UserSubscription (
    UserID INT NOT NULL,
    SubscriptionID INT NOT NULL,
    Status ENUM('Pending', 'Active', 'Expired') DEFAULT 'Pending',
    StartDate DATE NOT NULL,
    PRIMARY KEY (UserID, SubscriptionID),
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (SubscriptionID) REFERENCES Subscription(SubscriptionID) ON DELETE CASCADE
);

-- =========================
-- 7. Listener
-- =========================
CREATE TABLE Listener (
    ListenerID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL UNIQUE,
    Preference VARCHAR(255),
    FavoriteGenre VARCHAR(100),
    LikedArtwork TEXT COMMENT 'Historical/legacy reference only',
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
);

-- =========================
-- 8. Artist
-- =========================
CREATE TABLE Artist (
    ArtistID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL UNIQUE,
    LabelID INT,
    Genre VARCHAR(100),
    VerifiedStatus ENUM('Pending', 'Verified', 'Rejected') DEFAULT 'Pending',
    TotalFollowers INT DEFAULT 0,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (LabelID) REFERENCES Label(LabelID) ON DELETE SET NULL
);

-- =========================
-- 9. Artist_SMLinks
-- =========================
CREATE TABLE Artist_SMLinks (
    ArtistID INT PRIMARY KEY,
    SMLinks JSON COMMENT 'JSON array of social media links',
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID) ON DELETE CASCADE
);

-- =========================
-- 10. Artwork
-- =========================
CREATE TABLE Artwork (
    ArtworkID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(100) NOT NULL,
    ReleaseDate DATE,
    CoverImage VARCHAR(255),
    Duration INT NOT NULL,
    Genre VARCHAR(100)
);

-- =========================
-- 11. Album
-- =========================
CREATE TABLE Album (
    AlbumID INT AUTO_INCREMENT PRIMARY KEY,
    ArtworkID INT NOT NULL,
    TotalTrack INT DEFAULT 0,
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- =========================
-- 12. Single
-- =========================
CREATE TABLE Single (
    SingleID INT AUTO_INCREMENT PRIMARY KEY,
    ArtworkID INT NOT NULL,
    AlbumID INT,
    TrackNumber INT,
    FileURL VARCHAR(500),
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- =========================
-- 13. Playlist
-- =========================
CREATE TABLE Playlist (
    PlaylistID INT AUTO_INCREMENT PRIMARY KEY,
    ListenerID INT NOT NULL,
    Name VARCHAR(255) NOT NULL,
    CreateDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ListenerID) REFERENCES Listener(ListenerID) ON DELETE CASCADE
);

-- =========================
-- 14. Contain
-- =========================
CREATE TABLE Contain (
    PlaylistID INT NOT NULL,
    SingleID INT NOT NULL,
    PRIMARY KEY (PlaylistID, SingleID),
    FOREIGN KEY (PlaylistID) REFERENCES Playlist(PlaylistID) ON DELETE CASCADE,
    FOREIGN KEY (SingleID) REFERENCES Single(SingleID) ON DELETE CASCADE
);

-- =========================
-- 15. PlayHistory
-- =========================
CREATE TABLE PlayHistory (
    PlayHistoryID INT AUTO_INCREMENT PRIMARY KEY,
    ListenerID INT NOT NULL,
    ArtworkID INT NOT NULL,
    PlayedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ListenerID) REFERENCES Listener(ListenerID) ON DELETE CASCADE,
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID) ON DELETE CASCADE
);

-- =========================
-- 16. Follow
-- =========================
CREATE TABLE Follow (
    ListenerID INT NOT NULL,
    ArtistID INT NOT NULL,
    PRIMARY KEY (ListenerID, ArtistID),
    FOREIGN KEY (ListenerID) REFERENCES Listener(ListenerID) ON DELETE CASCADE,
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID) ON DELETE CASCADE
);

-- =========================
-- 17. React
-- =========================
CREATE TABLE React (
    ListenerID INT NOT NULL,
    ArtworkID INT NOT NULL,
    PRIMARY KEY (ListenerID, ArtworkID),
    FOREIGN KEY (ListenerID) REFERENCES Listener(ListenerID) ON DELETE CASCADE,
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID) ON DELETE CASCADE
);

-- =========================
-- 18. Release
-- =========================
CREATE TABLE ReleaseTable (
    ReleaseID INT AUTO_INCREMENT PRIMARY KEY,
    ArtistID INT NOT NULL,
    ArtworkID INT NOT NULL,
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID) ON DELETE CASCADE,
    FOREIGN KEY (ArtworkID) REFERENCES Artwork(ArtworkID) ON DELETE CASCADE,
    UNIQUE KEY uk_artist_artwork (ArtistID, ArtworkID)
);

-- =========================
-- 19. Collaboration
-- =========================
CREATE TABLE Collaboration (
    CollaborationID INT AUTO_INCREMENT PRIMARY KEY,
    ArtistID_1 INT NOT NULL COMMENT 'Main artist',
    ArtistID_2 INT NOT NULL COMMENT 'Collaborating artist',
    SingleID INT NOT NULL,
    FOREIGN KEY (ArtistID_1) REFERENCES Artist(ArtistID) ON DELETE CASCADE,
    FOREIGN KEY (ArtistID_2) REFERENCES Artist(ArtistID) ON DELETE CASCADE,
    FOREIGN KEY (SingleID) REFERENCES Single(SingleID) ON DELETE CASCADE,
    UNIQUE KEY uk_collaboration (ArtistID_1, ArtistID_2, SingleID)
);




