import React, { Fragment } from 'react';
import { Image } from 'react-bootstrap';
import ReactPlayer from "react-player";

class MixedMedia extends React.Component {
  
  render() {
    function getUrlsForImages(items, props) {
      if (Array.isArray(items)) {
        if (items[0].endsWith("master.m3u8")) {
          return (
            <Fragment>
              <ReactPlayer className="foreground-item" url={items[0]} playing width="100%" height="100%" loop={props? props.event.loop : false} />
              <Image className="background-item" src={items[1]} fluid />
            </Fragment>)
        }
        return <div><Image className="foreground-item" src={items[0]} fluid/><Image className="background-item" src={items[1]} fluid/></div>
      } 
      return <div><Image src={items} fluid/></div>
    };
    
    return (
      <Fragment>
          {this.props.imageUrl ? getUrlsForImages(this.props.imageUrl, this.props) : null }
          {this.props.text ? <div>{this.props.text}</div> : null}
      </Fragment>
    );
  }
}

export default MixedMedia;


