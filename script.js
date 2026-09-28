const chatbox = document.getElementById("chatbox");

function addMessage(message, sender) {

    const div = document.createElement("div");

    div.className = sender;

    div.innerText = message;

    chatbox.appendChild(div);

    chatbox.scrollTop = chatbox.scrollHeight;
}


// Complaint
function complaint() {

    addMessage("I want to register a complaint.", "user");

    addMessage(
        "Sure! Please provide your complaint details. " +
        "Example: Water shortage in Room 205.",
        "bot"
    );
}


// Room allocation
function roomAllocation() {

    addMessage("I have a room allocation query.", "user");

    addMessage(
        "Available rooms can be checked through the hostel office. " +
        "Please provide your year, department and preferred hostel.",
        "bot"
    );
}


// Maintenance
function maintenance() {

    addMessage("I want to report a maintenance problem.", "user");

    addMessage(
        "Please describe the problem and mention your room number. " +
        "Example: Fan not working in Room 205.",
        "bot"
    );
}


// Facilities
function facilities() {

    addMessage("What facilities are available?", "user");

    addMessage(
        "Hostel facilities include:\n" +
        "• Wi-Fi\n" +
        "• Drinking water\n" +
        "• Study room\n" +
        "• Laundry\n" +
        "• Mess\n" +
        "• Common room\n" +
        "• Sports facilities",
        "bot"
    );
}


// Normal text query
function sendMessage() {

    const input = document.getElementById("userInput");

    const message = input.value.trim();

    if (message === "") return;

    addMessage(message, "user");

    input.value = "";

    const text = message.toLowerCase();

    let reply =
        "Sorry, I couldn't understand your query. " +
        "Please select Complaint, Room Allocation, " +
        "Maintenance or Facilities.";

    if (text.includes("complaint") ||
        text.includes("complain")) {

        reply =
            "Please provide your complaint details and room number. " +
            "Your complaint will be forwarded to the hostel administration.";
    }

   // Maintenance
else if (text.includes("maintenance") ||
         text.includes("repair") ||
         text.includes("fan") ||
         text.includes("light") ||
         text.includes("water") ||
         text.includes("plumbing") ||
         text.includes("leak") ||
         text.includes("electricity")) {

    reply =
        "This appears to be a maintenance issue. " +
        "Please provide your room number and describe the problem. " +
        "Example: Water shortage in Room 205.";
}

// Room Allocation
else if (text.includes("room allocation") ||
         text.includes("room allotment") ||
         text.includes("vacancy") ||
         text.includes("available room") ||
         text.includes("hostel room")) {

    reply =
        "For room allocation, please provide your year, " +
        "department and preferred hostel.";
}
    else if (text.includes("facility") ||
             text.includes("wifi") ||
             text.includes("mess") ||
             text.includes("laundry")) {

        reply =
            "Hostel facilities include Wi-Fi, mess, laundry, " +
            "drinking water, study room and common room.";
    }

    setTimeout(function() {

        addMessage(reply, "bot");

    }, 500);
}
