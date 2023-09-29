import React from 'react';

class DataTable extends React.Component {
  render() {
    const { data } = this.props;

    // Convert the dictionary keys into an array to iterate over
    const keys = Object.keys(data);

    return (
      <table>
        <thead>
          <tr>
            <th>Key</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {keys.map((key) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{data[key]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  }
}

export default DataTable;
