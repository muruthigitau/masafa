import React from "react";

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="py-1">
      <div className="w-full px-2 mx-auto text-xs">
        <div className="hidden md:flex md:flex-row items-center gap-2 -mx-3 lg:justify-between">
          <div className="w-fit px-3 mt-0 shrink-0">
            <div className="text-sm leading-normal text-center text-slate-500 lg:text-left">
              Made with <i className="fa fa-heart text-pink-600"></i> by
              <a
                href="https://softleek.com/"
                className="font-semibold text-blue-700"
                target="_blank"
                rel="noopener noreferrer"
              >
                &nbsp;Softleek&nbsp;
              </a>
              for a better web.
            </div>
          </div>
          <div>&copy; {currentYear} All rights reserved.</div>
          <div className="w-fit px-3 mt-0 shrink-0">
            <ul className="flex flex-wrap justify-center pl-0 mb-0 list-none lg:justify-end">
              <li className="nav-item">
                <a
                  href="/"
                  className="block px-4 pt-0 pb-1 text-sm font-normal transition-colors ease-soft-in-out text-slate-500"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  About Us
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
