import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import LandingPage from '@pages/Landing/LandingPage'
import Login from '@pages/Auth/Login'
import Signup from '@pages/Auth/Signup'
import HomePage from '@pages/Home/HomePage'

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
  }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
)
