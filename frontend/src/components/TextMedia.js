import React from 'react';
import { Breadcrumb } from 'react-bootstrap'

class TextMedia extends React.Component {
  render() {
    // console.log('TextMedia received:');
    // console.log(this.props);
    return (
      <div className='TextMedia'>
      <Breadcrumb>
        <Breadcrumb.Item>{this.props.text}</Breadcrumb.Item>
      </Breadcrumb>
      </div>
    );
  }
}

export default TextMedia;
