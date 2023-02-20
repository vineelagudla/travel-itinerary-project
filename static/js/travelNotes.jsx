
function TravelNotes(props) {

    const [note, setNoteValue] = React.useState("");
    const [currentNotes, setCurrentNotes] = React.useState([]);

    React.useEffect(() => {
        let isMounted = true;
        fetch('/get-travel-notes')
            .then((response) => response.json())
            .then((result) => {
                if (result && isMounted) {
                    setCurrentNotes([result]);
                }
            });
        return () => { isMounted = false };
    }, []);

    const handleChange = (event) => {
        setNoteValue(event.target.value);
    }

    const handleNewNote = (event) => {
        setCurrentNotes([event.target.value]);
    }
    const handleAddNotesClick = () => {
        //setNoteValue(note);
        console.log(note);
        setCurrentNotes([...currentNotes, note]);
        setNoteValue("");
    }
    const handleUpdateNotesClick = () => {
        //navigate(`/travel-notes?notes=${currentNotes}`);
        let updateNotesDB = currentNotes.join(".\n");
        fetch("/travel-notes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            // this could also be written as body: JSON.stringify({ name, skill }) with 
            // JS object property value shorthand
            body: JSON.stringify({
                "newNotes": updateNotesDB
            }),
        })
            .then((response) => response.text())
            .then((jsonResponse) => {
            });
    }
    let newNotes = currentNotes.join(".\n");

    return (
        <div className="TravelNotes">
            <b><label htmlFor="add notes" className="add-notes">Notes:</label></b>
            <input
                type="text"
                //<textarea
                className="add-notes"
                id="note"
                name="note"
                placeholder="Add notes to your trip"
                onChange={handleChange}
                value={note}
            />
            <button className="notes-btn" onClick={handleAddNotesClick}>Add notes</button>
            <br></br>
            <br></br>
            <label>
                <b>Show my notes:
                    <textarea
                        className="show-notes"
                        name="notes-ta"
                        onChange={handleNewNote}
                        value={newNotes}
                        
                    /></b>
            </label>
            <br></br>
            <button className="update-notes-btn" onClick={handleUpdateNotesClick}>Update notes</button>
            <br></br><br></br>
        </div>
    );
}

ReactDOM.render(<TravelNotes />, document.querySelector('#root'));
