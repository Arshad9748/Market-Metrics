import React from "react";
import Sales1 from "../assets/Sales1.jpg";
//about section component
const About = () => {
  return (
    <div id="about" className="bg-neutral-900 text-white min-h-[600px] grid place-items-center py-12 sm:py-16 duration-300">
      <div className="container px-4 sm:px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 place-items-center gap-8">
          <div className="order-2 md:order-1">
            <img
              src={Sales1}
              alt="Sales"
              className="w-full max-w-[400px] md:scale-110 md:-translate-x-8 max-h-[300px] drop-shadow-[2px_10px_6px_rgba(0,0,0,0.50)]"
            />
          </div>
          <div className="order-1 md:order-2">
            <div className="space-y-5 p-4 sm:p-8">
              <h1 className="text-3xl sm:text-4xl font-bold font-serif text-center text-[#D50B8B]">
                ABOUT
              </h1>
              <p className="leading-7 sm:leading-8 tracking-wide text-base sm:text-lg">
                Sales prediction, also known as sales forecasting, is the
                process of estimating a business's future sales or revenue.
                It involves analyzing historical sales data, market trends,
                and other relevant factors to identify patterns and trends that
                can be used to make predictions.
              </p>
              <p className="text-base sm:text-lg">
                Sales forecasting can help businesses plan, allocate resources,
                and identify opportunities and risks.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
