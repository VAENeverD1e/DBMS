import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import { MainLayout } from '@components/layout'
import { PlaylistProvider } from '@contexts/PlaylistContext'
import { ToastProvider } from '@contexts/ToastContext'
import LandingPage from '@pages/Landing/LandingPage'
import Login from '@pages/Auth/Login'
import Signup from '@pages/Auth/Signup'
import HomePage from '@pages/Home/HomePage'
import SubscriptionPage from '@pages/Subscription/SubscriptionPage'
import ListenerSubscriptionPage from '@pages/Subscription/ListenerSubscriptionPage'
import ArtistSubscriptionPage from '@pages/Subscription/ArtistSubscriptionPage'
import ListenerHomePage from '@pages/Listener/ListenerHomePage'
import AlbumDetailPage from '@pages/Album/AlbumDetailPage'
import ArtistProfilePage from '@pages/Artist/ArtistProfilePage'
import ArtistHomePage from '@pages/Artist/ArtistHomePage'
import ArtistArtworkDetailPage from '@pages/Artist/ArtistArtworkDetailPage'
import UserProfilePage from '@pages/Profile/UserProfilePage'
import PlaylistDetailPage from '@pages/Playlist/PlaylistDetailPage'

const router = createBrowserRouter([
  {
    element: <MainLayout />,
    children: [
      {
        element: <LandingPage />,
        path: '/'
      },
      {
        element: <Login />,
        path: '/login'
      },
      {
        element: <Signup />,
        path: '/signup'
      },
      {
        element: <HomePage />,
        path: '/home'
      },
      {
        element: <SubscriptionPage />,
        path: '/subscription'
      },
      // Listener routes
      {
        element: <ListenerHomePage />,
        path: '/listener/home'
      },
      {
        element: <ListenerHomePage />,
        path: '/listener'
      },
      {
        element: <ListenerSubscriptionPage />,
        path: '/listener/subscription'
      },
      {
        element: <AlbumDetailPage />,
        path: '/listener/album/:id'
      },
      {
        element: <ArtistProfilePage />,
        path: '/listener/artist/:id'
      },
      {
        element: <ArtistHomePage />,
        path: '/artist-home'
      },
      {
        element: <ArtistArtworkDetailPage />,
        path: '/artist/artwork/:id'
      },
      {
        element: <UserProfilePage />,
        path: '/listener/profile'
      },
      {
        element: <PlaylistDetailPage />,
        path: '/listener/playlist/:id'
      },
      // Artist routes
      {
        element: <ArtistHomePage />,
        path: '/artist/home'
      },
      {
        element: <ArtistSubscriptionPage />,
        path: '/artist/subscription'
      },
      {
        element: <ArtistArtworkDetailPage />,
        path: '/artist/artwork/:id'
      }
    ]
  }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ToastProvider>
      <PlaylistProvider>
        <RouterProvider router={router} />
      </PlaylistProvider>
    </ToastProvider>
  </StrictMode>
)
