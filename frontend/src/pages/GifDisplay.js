import React, { useState } from 'react';

function GifDisplay() {
  const [showGif, setShowGif] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  const handleClick = () => {
    setIsVisible(!isVisible);
    setShowGif(!showGif);
  };

  return (
    <div>
      <button className="buttonComponent" onClick={handleClick}
      style={{ opacity: isVisible ? 100 : 0 }}> ^</button>
      {showGif && (
        <div>
            <img
            src="https://media.giphy.com/media/KMqXzclJWF3373gmyG/giphy-downsized-large.gif" 
            alt="Your GIF"
            />
            <img
            src="https://media.giphy.com/media/FsS6wi25NTAuOrI80T/giphy-downsized-large.gif" 
            alt="Your GIF"
            />
            <img
            src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2I2a2NpdmNwMmVrZmlidmk3cW1ienVhd2F1cTRmM3ZsMnh4MWdiaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Dx6FC4JvGDTbdhsOfz/giphy-downsized-large.gif" // Replace with the path to your GIF
            alt="Your GIF"
            />
        </div>
      ) }
    </div>
  );
}

export default GifDisplay;
