import React from 'react';
import io from 'socket.io-client';

// const socket = io({
//   forceNew: true,
//   transport: ['websocket'],
//   transportOptions: {
//     polling: {
//       extraHeaders: {
//       }
//     }
//   }
// });

const socket = io({
  transport: ['websocket'],
  transportOptions: {
    polling: {
      extraHeaders: {
      }
    }
  }
});

class CourseConnection extends React.Component {
  componentDidMount() {
    socket.on('connect', socket => {
    console.log("CourseConnection: socket.on('connect') received.");
    this.setState({'client': socket, 'connected': true});
    });
    socket.on('reconnect_attempt', () => {
      socket.io.opts.transports = ['polling', 'websocket'];
    });
    socket.on('message', message => {
        console.log("CourseConnection: socket.on('message') received");
        // todo: Do something else with messages...
        this.props.msgCallbackFromParent(message);
    });
     // Expects JSON
     //  todo: had to modify to work with admin interface
    socket.on('event', event => {
        console.log("CourseConnection: socket.on('event') received");
        this.setState({'event': event});
        this.props.eventCallbackFromParent(event);
    });
    socket.on('disconnect', client => {
        console.log("CourseConnection: socket.on('disconnect') received");
        this.setState({'client': client, 'connected': false});
    });
    socket.on('error', error => {
       console.log(socket.id + ' error: ' + error)
    });
    socket.on('connect_error', error => {
       console.log(socket.id + ' connect error: ' + error)
    });
    socket.on('connect_timeout', error => {
       console.log(socket.id +  ' client timeout: ' + error)
    });
  }
  render() {
      return null
  }
}
export default CourseConnection;
