// import Button from 'react-bootstrap/Button';
// import Collapse from 'react-bootstrap/Collapse';

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
            <div className="row">
                <div className="col-4">
                    <b><label htmlFor="add notes" className="add-notes">Note&nbsp;&nbsp;</label></b>
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
                    <button className="notes-btn" onClick={handleAddNotesClick}>+</button>
                    <br></br>
                    <br></br>
                </div>
                <div className="col-6">
                    <div className="row">
                        <div className="col-3">
                            Trip Notes
                        </div>
                        <div className="col-7">
                            <textarea
                                name="notes-ta"
                                onChange={handleNewNote}
                                value={newNotes}
                                cols={25}
                            />
                        </div>
                        <div className="col-2">
                            <button className="update-notes" onClick={handleUpdateNotesClick}>&nbsp;Update Notes</button>
                        </div>
                    </div>
                </div>
                <div className="col-2"></div>
                <br></br><br></br>
            </div>
        </div>
    );
}

ReactDOM.render(<TravelNotes />, document.querySelector('#root'));
