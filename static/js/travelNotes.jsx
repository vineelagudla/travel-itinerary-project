function TravelNotes() {
    return (
        <div className="TravelNotes">
            <b><label htmlFor="add notes" className="add-notes">Notes:</label></b>
            <input
                type="text"
                className="add-notes"
                id="note"
                name="note"
                placeholder="Add notes to your trip"
            />

            <button className="notes-btn">Add notes</button>
            <br></br>
            <br></br>
            <b>Show my notes:<textarea className="show-notes" name="notes-ta" readonly></textarea></b>
            <br></br>
        </div>
    );
}

ReactDOM.render(<TravelNotes />, document.querySelector('#root'));
