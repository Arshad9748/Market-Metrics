import React from "react";
import { RiUserSmileFill } from "react-icons/ri";
import { GiNotebook } from "react-icons/gi";
import { GoGraph } from "react-icons/go";

const skillsData = [
  {
    name: "User Friendly",
    icon: <RiUserSmileFill className="text-4xl sm:text-5xl text-primary" />,
    link: "#",
  },
  {
    name: "Fast and Safe",
    icon: <GiNotebook className="text-4xl sm:text-5xl text-primary" />,
    link: "#",
  },
  {
    name: "Accurate Predictions",
    icon: <GoGraph className="text-4xl sm:text-5xl text-primary" />,
    link: "#",
  },
];

const Services = () => {
  return (
    <div id="services" className="py-16 sm:pt-40 sm:pb-30 bg-black text-white">
      <div className="container mx-auto px-4 sm:px-6">
        <div className="pb-8 sm:pb-12">
          <h1 className="text-2xl sm:text-3xl font-semibold text-center font-serif">
            Why Choose Us
          </h1>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {skillsData.map((skill) => (
            <div
              key={skill.name}
              className="card text-center space-y-4 sm:space-y-6 p-4 sm:p-6 bg-neutral-900 rounded-lg hover:bg-[#D50B8B] hover:text-white transition duration-300"
            >
              <div className="grid place-items-center">{skill.icon}</div>
              <h1 className="text-xl sm:text-2xl font-bold">{skill.name}</h1>
              <a
                href={skill.link}
                className="inline-block text-base sm:text-lg font-semibold text-[#D50B8B] hover:text-white transition duration-300"
              >
                Learn more
              </a>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Services;
