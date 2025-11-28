import React, { useState, useEffect } from "react";
import artworksService from "../../services/artworksService";
import playlistService from "../../services/playlistService";
import artistService from "../../services/artistService";

const FALLBACK_IMAGE =
  "https://via.placeholder.com/300x300/F6A661/3E3B2C?text=Artwork";

/**
 * RightSidebar Component
 * Reusable right sidebar with current song, upcoming song, artist info, and related artworks
 * Now with internal logic to calculate upcoming songs and fetch related artworks
 */
const RightSidebar = ({
  currentSong = {
    title: "Song name",
    artist: "Artist name",
    image: "/Artwork_cover.png",
  },
  playbackContext = null, // { type: 'album'|'playlist'|'single', id: number, songs: Array, currentIndex: number }
  artistInfo = {
    name: "Red Velvet",
    description:
      "Red Velvet is a South Korean girl group formed by SM Entertainment in 2014. The group is known for its versatile music style and dual concept — the 'Red' side represents bright, energetic pop and dance music, while the 'Velvet' side showcases smooth R&B and soulful sounds. With hits like 'Bad Boy,' 'Red Flavor,' and 'Psycho,' Red Velvet has gained international recognition for their vocal talent, innovative concepts, and diverse discography.",
    image: "/WelcomeTo.png",
    buttonLabel: "Follow",
  },
}) => {
  const [upcomingSong, setUpcomingSong] = useState(null);
  const [relatedArtworks, setRelatedArtworks] = useState([]);

  // Effect to calculate upcoming song from playback context
  useEffect(() => {
    if (!playbackContext) {
      setUpcomingSong(null);
      return;
    }

    const { type, songs, currentIndex } = playbackContext;

    // Only show upcoming song for albums and playlists, not singles
    if (type === 'single') {
      setUpcomingSong(null);
      return;
    }

    // Check if there's a next song in the list
    if (songs && Array.isArray(songs) && currentIndex !== undefined) {
      const nextIndex = currentIndex + 1;
      if (nextIndex < songs.length) {
        const nextSong = songs[nextIndex];
        setUpcomingSong({
          title: nextSong.title || nextSong.Title || "Unknown Song",
          artist: nextSong.artist || nextSong.Artist || nextSong.ArtistName || "Unknown Artist",
          image: nextSong.image || nextSong.CoverImage || nextSong.cover_image || "/ArtworkImage1.png",
        });
      } else {
        setUpcomingSong(null);
      }
    } else {
      setUpcomingSong(null);
    }
  }, [playbackContext]);

  // Effect to fetch related artworks by artist
  useEffect(() => {
    const fetchRelatedArtworks = async () => {
      if (!currentSong || !currentSong.artistId) {
        setRelatedArtworks([]);
        return;
      }

      try {
        const response = await artistService.getArtistArtworks(currentSong.artistId, {
          limit: 5,
          offset: 0,
        });

        if (response && response.artworks && Array.isArray(response.artworks)) {
          // Filter out the current artwork if it's in the list
          const filteredArtworks = response.artworks
            .filter(artwork => artwork.ArtworkID !== currentSong.artworkId)
            .slice(0, 4) // Limit to 4 related artworks
            .map(artwork => ({
              id: artwork.ArtworkID || artwork.artwork_id,
              name: artwork.Title || artwork.title || "Unknown Artwork",
              image: artwork.CoverImage || artwork.cover_image || "/ArtworkImage1.png",
            }));

          setRelatedArtworks(filteredArtworks);
        } else {
          setRelatedArtworks([]);
        }
      } catch (error) {
        console.error("Error fetching related artworks:", error);
        setRelatedArtworks([]);
      }
    };

    fetchRelatedArtworks();
  }, [currentSong?.artistId, currentSong?.artworkId]);

  return (
    <div className="w-90 bg-black rounded-xl border-l-4 flex flex-col overflow-hidden">
      {/* Current Song Album Art */}
      <div className="p-6">
        <img
          src={currentSong.image}
          alt={currentSong.title}
          className="w-full aspect-square rounded-lg mb-4 object-cover"
          onError={(e) => {
            // e.target.src = FALLBACK_IMAGE;
          }}
        />
        <div className="mb-2">
          <p className="text-white text-xl font-bold">{currentSong.title}</p>
          <p className="text-gray-400 text-sm">{currentSong.artist}</p>
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto px-6 pb-6 scrollbar-hide">
        {/* Upcoming Song - Only show if upcomingSong exists */}
        {upcomingSong && upcomingSong.title && (
          <div className="mb-6">
            <h3 className="text-white font-bold mb-3">Upcoming Song:</h3>
            <div className="flex items-center gap-3 bg-[#F6A661] rounded-lg p-2">
              <img
                src={upcomingSong.image}
                alt={upcomingSong.title}
                className="w-10 h-10 rounded object-cover"
                onError={(e) => {
                  // e.target.src =
                  //   "https://via.placeholder.com/64x64/3E3B2C/F6A661?text=Upcoming";
                }}
              />
              <div className="flex-1">
                <p className="text-white text-sm font-semibold">
                  {upcomingSong.title}
                </p>
                <p className="text-gray-300 text-xs">{upcomingSong.artist}</p>
              </div>
            </div>
          </div>
        )}

        {/* About Artist */}
        <div className="mb-6 rounded-lg border-t-2 border-b-2 border-[#F6A661] bg-[#2A2820] p-4">
          <h3 className="text-white font-bold mb-3">About Artist:</h3>
          <img
            src={artistInfo.image}
            alt={artistInfo.name}
            className="w-full h-32 object-cover rounded-lg mb-3"
            onError={(e) => {
              // e.target.src =
              //   "https://via.placeholder.com/300x128/3E3B2C/F6A661?text=Artist";
            }}
          />
          <div className="bg-[#F6A661] rounded-lg p-4">
            <div className="flex items-center justify-between mb-4">
              <h4 className="text-[#3E3B2C] text-2xl font-bold">
                {artistInfo.name}
              </h4>
              {artistInfo.buttonLabel && (
                <button className="bg-white border-2 border-black text-black px-4 py-0.5 rounded-full text-sm font-bold hover:bg-gray-100 transition-colors">
                  {artistInfo.buttonLabel}
                </button>
              )}
            </div>
            <p className="text-[#3F3C35] text-xs leading-relaxed">
              {artistInfo.description}
            </p>
          </div>
        </div>

        {/* Related Artworks */}
        {relatedArtworks.length > 0 && (
          <div>
            <h3 className="text-white font-semibold mb-3">Related Artworks:</h3>
            <div className="space-y-3">
              {relatedArtworks.map((artwork) => (
                <div key={artwork.id} className="bg-[#2A2820] rounded-lg p-3">
                  <img
                    src={artwork.image}
                    alt={artwork.name}
                    className="w-full aspect-square object-cover rounded-lg mb-2"
                    onError={(e) => {
                      // e.target.src = FALLBACK_IMAGE;
                    }}
                  />
                  <p className="text-white text-sm font-semibold text-center">
                    {artwork.name}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RightSidebar;