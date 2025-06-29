import React from 'react';
import sales from '../assets/sl.png';

const Hero = () => {
  return (
    <div className="bg-black text-white px-4 sm:px-6 pt-20 sm:pt-32 pb-16 sm:pb-24 min-h-screen flex items-center justify-center">
      <div className="container mx-auto grid md:grid-cols-2 gap-8 md:gap-12 items-center">
        <div className="space-y-6 text-center md:text-left md:ml-12">
          <p className="text-xl sm:text-2xl font-serif text-[#D50B8B]">Effortless</p>
          <h1 className="text-4xl sm:text-5xl lg:text-7xl font-bold font-serif">
            Sales Prediction
          </h1>
          <p className="text-base sm:text-lg leading-relaxed">
            A thorough and believable sales forecast is the cornerstone of your business plan and financial projections.
          </p>
        </div>
        <div className="flex justify-center md:justify-end lg:ml-60 mt-8 md:mt-0">
          <img
            src={sales}
            alt="Sales"
            className="max-h-[200px] sm:max-h-[300px] w-full object-contain"
          />
        </div>
      </div>
    </div>
  );
};

export default Hero;
