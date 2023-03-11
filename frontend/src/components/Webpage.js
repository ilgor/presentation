import React from 'react';

class Webpage extends React.Component {
  render() {
    return (
      <div>
        {this.props.webUrl ? <iframe className="webpage" src={this.props.webUrl} frameborder="0" allow="autoplay" allowfullscreen></iframe> : null }
      </div>
    );
  }
}

export default Webpage;


