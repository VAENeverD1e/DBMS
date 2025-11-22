import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import LandingPage from '@pages/Landing/LandingPage'
import Login from '@pages/Auth/Login'
import Signup from '@pages/Auth/Signup'
import HomePage from '@pages/Home/HomePage'
import SubscriptionPage from '@pages/Subscription/SubscriptionPage'
import ListenerHomePage from '@pages/Listener/ListenerHomePage'
import AlbumDetailPage from '@pages/Album/AlbumDetailPage'
import ArtistProfilePage from '@pages/Artist/ArtistProfilePage'
import ArtistHomePage from '@pages/Artist/ArtistHomePage'
import ArtistArtworkDetailPage from '@pages/Artist/ArtistArtworkDetailPage'
import UserProfilePage from '@pages/Profile/UserProfilePage'

const router = createBrowserRouter([
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
  {
    element: <ListenerHomePage />,
    path: '/listener'
  },
  {
    element: <AlbumDetailPage />,
    path: '/album/:id'
  },
  {
    element: <ArtistProfilePage />,
    path: '/artist/:id'
  },
  {
    element: <ArtistHomePage />,
    path: '/artist/home'
  },
  {
    element: <ArtistArtworkDetailPage />,
    path: '/artist/artwork/:id'
  },
  {
    element: <UserProfilePage />,
    path: '/profile'
  }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
)
