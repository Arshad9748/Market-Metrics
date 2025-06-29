import React from "react";
import {
  FaFacebook,
  FaInstagram,
  FaLinkedin,
  FaLocationArrow,
  FaMobileAlt,
} from "react-icons/fa";

const FooterLinks = [
  { title: "Home", link: "/#" },
  { title: "About", link: "/#about" },
  { title: "Services", link: "/#services" },
];

const Footer = () => {
  return (
    <div id="contact" className="bg-black pt-30 pb-16 text-white">
      <section className="max-w-6xl mx-auto px-4 py-10">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h1 className="text-2xl font-bold mb-3 font-serif">Sales Prediction</h1>
            <p className="text-sm mb-4">
              A thorough and believable sales forecast is the cornerstone of
              your business plan and financial projections.
            </p>
            <div className="flex items-center gap-2 text-sm mb-2">
              <FaLocationArrow />
              <p>Kolkata, West Bengal</p>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <FaMobileAlt />
              <p>+91 **********</p>
            </div>
            <div className="flex gap-4 mt-4 text-xl">
              <a href="#"><FaInstagram className="hover:text-pink-500 transition" /></a>
              <a href="#"><FaFacebook className="hover:text-pink-600 transition" /></a>
              <a href="#"><FaLinkedin className="hover:text-pink-800 transition" /></a>
            </div>
          </div>
          <div>
            <h2 className="text-xl font-semibold mb-3">Quick Links</h2>
            <ul className="flex flex-col gap-2">
              {FooterLinks.map((link, index) => (
                <li key={index}>
                  <a
                    href={link.link}
                    className="hover:translate-x-1 hover:text-[#D50B8B] transition block"
                  >
                    &#11162; {link.title}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Footer;
