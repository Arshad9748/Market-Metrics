import React from 'react';
import Navbar from './Navbar';
import Hero from './Hero';
import About from './About';
import Services from './Services';
import Footer from './Footer';


function Landingpage() {
    return (
        <div>
            <Navbar />
            <Hero />
            <About />
            <Services />
            <Footer />

        </div>
    );
}
export default Landingpage;