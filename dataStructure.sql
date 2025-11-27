-- ============================================================
-- DATA INSERTION SCRIPT (Listener vs Artist Plans)
-- ============================================================

SET FOREIGN_KEY_CHECKS = 0;

-- 1. Insert Labels
INSERT INTO Label (Name, ContactEmail, Country, FoundedYear) VALUES
('Global Records', 'contact@globalrecords.com', 'USA', 1995),
('Indie Vibe', 'hello@indievibe.co.uk', 'UK', 2010);

-- 2. Insert Subscriptions (UPDATED BASED ON YOUR REQUEST)
-- ID 1 = Listener Plan, ID 2 = Artist Plan
INSERT INTO Subscription (Name, Price, Duration, Type) VALUES
('Listener Premium', 9.99, 30, 'Listener'), -- ID 1
('Artist Pro Unlimited', 19.99, 30, 'Artist'); -- ID 2

-- 3. Insert Users
INSERT INTO User (Email, Password, Username, FirstName, LastName, Role) VALUES
('alice@listener.com', 'hash123', 'alice_music', 'Alice', 'Smith', 'Listener'), -- UserID 1
('bob@listener.com', 'hash456', 'bob_tunes', 'Bob', 'Jones', 'Listener'),    -- UserID 2
('weeknd@artist.com', 'hash789', 'the_weeknd', 'Abel', 'Tesfaye', 'Artist'),  -- UserID 3
('dua@artist.com', 'hash000', 'dualipa', 'Dua', 'Lipa', 'Artist');           -- UserID 4

-- 4. Insert Listeners (Linked to Users 1 and 2)
INSERT INTO Listener (UserID, Preference, FavoriteGenre, LikedArtwork) VALUES
(1, 'High Quality Streaming', 'Pop', NULL),
(2, 'Offline Mode', 'Rock', NULL);

-- 5. Insert Artists (Linked to Users 3 and 4)
INSERT INTO Artist (UserID, LabelID, Genre, VerifiedStatus, TotalFollowers) VALUES
(3, 1, 'R&B', 'Verified', 5000000), 
(4, 1, 'Pop', 'Verified', 6000000);

-- 6. Insert Artist Social Media Links
INSERT INTO Artist_SMLinks (ArtistID, SMLinks) VALUES
(1, '["twitter.com/theweeknd", "instagram.com/theweeknd"]'),
(2, '["instagram.com/dualipa"]');

-- 7. Insert Artwork
INSERT INTO Artwork (Title, ReleaseDate, CoverImage, Duration, Genre) VALUES
('After Hours', '2020-03-20', 'img1.jpg', 3600, 'R&B'),      -- ID 1 (Album)
('Blinding Lights', '2019-11-29', 'img2.jpg', 200, 'Synthwave'); -- ID 2 (Single)

-- 8. Insert Album
INSERT INTO Album (ArtworkID, TotalTrack) VALUES
(1, 14);

-- 9. Insert Single
INSERT INTO Single (ArtworkID, AlbumID, TrackNumber, FileURL) VALUES
(2, 1, 9, 's3://music/blinding_lights.mp3');

-- 10. Insert ReleaseTable
INSERT INTO ReleaseTable (ArtistID, ArtworkID) VALUES
(1, 1),
(1, 2);

-- 11. Insert Orders (UPDATED)
-- Alice (Listener) buys Subscription 1 (Listener Plan)
-- The Weeknd (Artist) buys Subscription 2 (Artist Plan)
INSERT INTO Orders (UserID, SubscriptionID, OrderDate) VALUES
(1, 1, '2023-10-01 10:00:00'),
(3, 2, '2023-10-02 14:00:00');

-- 12. Insert Payment
INSERT INTO Payment (OrderID, Method, Status, Amount) VALUES
(1, 'Credit Card', 'Completed', 9.99),
(2, 'PayPal', 'Completed', 19.99);

-- 13. Insert UserSubscription (UPDATED)
-- Connects the User to the specific plan they bought
INSERT INTO UserSubscription (UserID, SubscriptionID, Status, StartDate) VALUES
(1, 1, 'Active', '2023-10-01'), -- Alice has Listener Plan
(3, 2, 'Active', '2023-10-02'); -- The Weeknd has Artist Plan

-- 14. Insert Playlists
INSERT INTO Playlist (ListenerID, Name) VALUES
(1, 'Alice Favorites');

-- 15. Insert Contain
INSERT INTO Contain (PlaylistID, SingleID) VALUES
(1, 1);

-- 16. Insert Follow
INSERT INTO Follow (ListenerID, ArtistID) VALUES
(1, 1); -- Alice follows The Weeknd

-- 17. Insert React
INSERT INTO React (ListenerID, ArtworkID) VALUES
(1, 2); -- Alice likes Blinding Lights

-- 18. Insert PlayHistory
INSERT INTO PlayHistory (ListenerID, ArtworkID) VALUES
(1, 2);

SET FOREIGN_KEY_CHECKS = 1;
SELECT 'Data inserted with specific Listener/Artist subscriptions.' AS Status;