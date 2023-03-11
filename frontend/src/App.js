import React, { Component } from "react";
import VideoMedia from "./components/VideoMedia";
import MixedMedia from "./components/MixedMedia";
import Webpage from "./components/Webpage";
import SoundMedia from "./components/SoundMedia";
import CourseConnection from "./components/CourseConnection";
import "./App.css";
import { Row, Col } from "react-bootstrap";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      message: null,
      event: null,
      connected: null,
      text: null,
      videoUrl: null,
      imageUrl: null,
      roomId: null,
      firstLoad: true,
      sound1: null,
      sound2: null
    };
  }

  // Events set state, Messages do not.
  readEvents = (dataFromChild) => {
    const eventData = dataFromChild;
    let state_update = {};
    state_update["event"] = dataFromChild;
    if ("text" in eventData) {
      state_update["text"] = eventData["text"];
    } else {
      state_update["text"] = null;
    }

    if ("videoUrl" in eventData) {
      if (state_update["videoUrl"] !== null) {
        state_update["videoUrl"] = eventData["videoUrl"];
        state_update["loop"] = eventData["loop"];
        state_update["thumb"] = eventData["thumb"];
      }
    } else {
      state_update["videoUrl"] = null;
    }

    if ("imageUrl" in eventData) {
      state_update["imageUrl"] = eventData["imageUrl"];
      state_update["loop"] = eventData["loop"];
    } else {
      state_update["imageUrl"] = null;
    }

    if ("audioUrl" in eventData) {
      if (!this.state.sound1) {
        state_update["sound1"] = eventData["audioUrl"];
        state_update["fadein1"] = parseInt(eventData["fadein"]);
        state_update["fadeout1"] = parseInt(eventData["fadeout"]);
      } else if (!this.state.sound2) {
        state_update["sound2"] = eventData["audioUrl"];
        state_update["fadein2"] = parseInt(eventData["fadein"]);
        state_update["fadeout2"] = parseInt(eventData["fadeout"]);
      } else {
        state_update["sound1"] = this.state.sound2;
        state_update["fadein1"] = parseInt(this.state.fadein2);
        state_update["fadeout1"] = parseInt(this.state.fadeout2);

        state_update["sound2"] = eventData["audioUrl"];
        state_update["fadein2"] = parseInt(eventData["fadein"]);
        state_update["fadeout2"] = parseInt(eventData["fadeout"]);
      }
      // state_update["audioUrl"].push(eventData["audioUrl"]);
      state_update["loop"] = eventData["loop"];
    } else {
      state_update["sound1"] = "";
      state_update["sound2"] = "";
    }

    if ("webUrl" in eventData) {
      state_update["webUrl"] = eventData["webUrl"];
    } else {
      state_update["webUrl"] = null;
    }
    this.setState(state_update);
  };

  readMessages = (dataFromChild) => {
    let title;
    try {
      title = dataFromChild.split("room_id: ")[1].split(",")[0];
    } catch (err) {
      title = "Room Id - Error";
    }
    document.title = title;
    this.setState({ message: dataFromChild, roomId: title});
  };

  InvalidData = (data) => {
    console.log(
      "Invalid JSON data schema sent from server: " + JSON.stringify(data)
    );
  };

  EventParser = (event) => {
    if (!("eventType" in event)) {
      return <this.InvalidData />;
    } else {
      switch (event["eventType"]) {
        case "TextMedia":
          return "Text";
        case "VideoMedia":
          return "Video";
        case "MixedMedia":
          return "Image";
        default:
          return "Webpage";
      }
    }
  };

  render() {
    if (this.state.event && this.state.event.background) {
      console.log(this.state.event.background);
      document.body.style = ("background: " + this.state.event.background);
    }

    const splitSlide = (props) => [
      <Row>
        <Col sm={6}><VideoMedia {...props} /></Col>
        <Col sm={6}><MixedMedia {...props} /></Col>
      </Row>,
    ];

    const currentSlide = (props) => {
      if (props.sound1 || props.sound2) {
        return (
          <Row>
            <Col sm={12}><SoundMedia {...props} /></Col>
          </Row>
        );
      }

      if (props.videoUrl && !props.imageUrl) {
        return (
          <Row>
            <Col sm={12}><VideoMedia {...props} /></Col>
          </Row>
        );
      }
      if (props.imageUrl) {
        return (
          <Row>
            <Col sm={12}><MixedMedia {...props} /></Col>
          </Row>
        );
      }
      if (props.webUrl) {
        return (
          <Row>
            <Col sm={12}><Webpage {...props} /></Col>
          </Row>
        );
      }
      if (!props.videoUrl && !props.imageUrl) {
        return <p></p>
      }
    };

    return (
      <div className="App">
        <CourseConnection msgCallbackFromParent={this.readMessages} eventCallbackFromParent={this.readEvents}/>
        {this.state.firstLoad ? (
          <div>
            <h3 className="white">Room ID: <i>{this.state.roomId}</i></h3>
              <button className="btn btn-success" onClick={() => this.setState({ firstLoad: false })}>START</button>
              {/* <br></br>
              <button className="btn btn-warning" onClick={() => window.location.href="/logout"}>Logout</button> */}
          </div>
        ) : (
          <div>{currentSlide(this.state)}</div>
        )}
      </div>
    );
  }
}

export default App;
