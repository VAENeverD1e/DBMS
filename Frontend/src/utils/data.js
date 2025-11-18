/**
 * Navigation items for the header menu
 * Each item has an id, label, and path (either '/' for home or '#section' for anchor links)
 */
export const HEADER_NAV_ITEMS = [
  { id: 1, label: 'Home', path: '/' },
  { id: 2, label: 'About Us', path: '#about' },
  { id: 3, label: 'Community', path: '#community' },
  { id: 4, label: 'Support', path: '#support' },
]

/**
 * Labels displayed below the community images
 * These describe the three main community features
 */
export const COMMUNITY_LABELS = [
  { id: 1, label: 'SUPPORT ARTISTS' },
  { id: 2, label: 'MUSIC CONNECTION' },
  { id: 3, label: 'FOR MUSIC LOVERS' },
]

/**
 * Hero section images - displayed in polaroid style on the right side
 * Images are positioned in a scattered layout with rotation
 * Note: Images should be placed in the /public folder
 */
export const HERO_IMAGES = [
  { id: 1, src: '/Singer.png', alt: 'Singer on stage' },
  { id: 2, src: '/Guitar.png', alt: 'Guitar player' },
  { id: 3, src: '/Drum.png', alt: 'Drum kit' },
]

/**
 * Community section images - displayed in polaroid style
 * These images appear below the "OUR COMMUNITY" heading
 * Note: Images should be placed in the /public folder
 */
export const COMMUNITY_IMAGES = [
  { id: 1, src: '/Guitar2.png', alt: 'Guitar player' },
  { id: 2, src: '/Singer.png', alt: 'Singer on stage' },
  { id: 3, src: '/Drum.png', alt: 'Drum kit' },
]

