import React, { Component } from "react";
import { Player, ControlBar, BigPlayButton } from "video-react";
import HLSSource from './HLSSource';
import "../../node_modules/video-react/dist/video-react.css"; // import css

export default class VideoMedia extends Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      playerSource: null,
      videoUrl: null,
    };
  }

  componentDidMount(prevProps, prevState) {
    if (prevProps !== this.props) {
      this.handleValueChange(this.props.videoUrl);
      this.updatePlayerInfo(this.props.videoUrl);
      this.player.load();
    }
    // this.player.toggleFullscreen(true);
    this.player.play();
    // this.player.toggleFullscreen(true);
  }

  componentDidUpdate(prevProps, prevState) {
    if (prevProps.videoUrl !== this.props.videoUrl) {
      this.handleValueChange(this.props.videoUrl);
      this.updatePlayerInfo(this.props.videoUrl);
      this.player.load();
    }
    // this.player.toggleFullscreen(true);
    this.player.play();
    // this.player.toggleFullscreen(true);
  }

  handleValueChange(value) {
    this.setState({
      videoUrl: value,
    });
  }

  updatePlayerInfo(value) {
    this.setState({
      playerSource: value,
    });
  }

  render() {
    let mediaSource;

    if (this.state.playerSource && this.state.playerSource.includes("master.m3u8")) {
      mediaSource = 
      <Player ref={(player) => { this.player = player; }} videoId={this.props.videoUrl} preload={true} autoPlay={true} fluid={true} playsInline={true} loop={this.props.event ? this.props.event.loop: false} volume={this.state.volume} poster={this.props.event ? this.props.event.thumb: null} className='poster-full'>
          <ControlBar className="video-react-control-bar-hide" autoHide={true} disableDefaultControls={true}></ControlBar>
          <BigPlayButton className="big-play-button-hide"> </BigPlayButton>
          <HLSSource isVideoChild src={this.state.playerSource} className='poster-full'/>
        </Player>;
    } else {
      mediaSource = 
      <Player ref={(player) => { this.player = player; }} videoId={this.props.videoUrl} preload={true} autoPlay={true} fluid={true} playsInline={true} loop={this.props.event ? this.props.event.loop: false} volume={this.state.volume}>
          <ControlBar className="video-react-control-bar-hide" autoHide={true} disableDefaultControls={true}></ControlBar>
          <BigPlayButton className="big-play-button-hide"> </BigPlayButton>
          <source src={this.state.playerSource} type="application/x-mpegURL"/>
        </Player>;
    }

    return (
      <div>
        { mediaSource }
      </div>
    );
  }
}
