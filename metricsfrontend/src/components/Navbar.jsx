import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import logo from '../assets/acme.svg'

export const Navlinks = [
  {
    id: 1,
    name: "HOME",
    link: "/#",
  },
  {
    id: 2,
    name: "ABOUT",
    link: "/#about",
  },
  {
    id: 3,
    name: "CONTACT",
    link: "/#contact",
  },
  {
    id: 4,
    name: "SERVICES",
    link: "/#services",
  },
];

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div>
      <header className='flex flex-row justify-between items-center p-4 bg-black text-white shadow-lg'>
        <Link to="/" className='flex items-center'>
          <img src={logo} alt="logo" className='h-10 w-10 mr-2' />
          <h1 className='text-2xl font-bold'>Market Metrics</h1>
        </Link>

        {/* Hamburger Menu Button */}
        <button 
          className='lg:hidden p-2'
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <div className='w-6 h-0.5 bg-white mb-1'></div>
          <div className='w-6 h-0.5 bg-white mb-1'></div>
          <div className='w-6 h-0.5 bg-white'></div>
        </button>

        {/* Desktop and Mobile Menu */}
        <div className={`${isMenuOpen ? 'flex' : 'hidden'} lg:flex flex-col lg:flex-row items-center gap-3 absolute lg:relative top-16 lg:top-0 left-0 right-0 bg-black lg:bg-transparent p-4 lg:p-0`}>
          <nav className='w-full lg:w-auto'>
            <ul className='flex flex-col lg:flex-row gap-4'>
              {Navlinks.map(({id,name,link}) => (
                <li key={id} className='p-4'>
                  <a 
                    href={link} 
                    className='text-lg font-semibold hover:text-[#D50B8B]'
                    onClick={() => setIsMenuOpen(false)}
                  >
                    {name}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
          <div className="flex flex-col lg:flex-row gap-3 w-full lg:w-auto">
          
            <Link
              to="/signin"
              className="px-4 py-4 bg-white text-[#D50B8B] rounded-lg font-semibold hover:bg-transparent hover:text-white border border-white  transition text-center"
              onClick={() => setIsMenuOpen(false)}
            >
              Login
            </Link>
          </div>
        </div>
      </header>
    </div>
  )
}

export default Navbar
