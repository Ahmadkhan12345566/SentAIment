<?php
header("Access-Control-Allow-Origin: *"); // Allow all origins
header("Access-Control-Allow-Methods: GET, POST, OPTIONS"); // Allow methods
header("Access-Control-Allow-Headers: Content-Type, Authorization"); // Allow headers
header("Content-Type: application/json"); // Set the content type to JSON

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit;
}

// Database connection setup
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "sen_chat";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die(json_encode(array("error" => "Connection failed: " . $conn->connect_error)));
}

// Retrieve and sanitize input data
$selectedUser = isset($_GET['user_id']) ? intval($_GET['user_id']) : 0;

if ($selectedUser > 0) {
    // Prepare SQL query to fetch messages for both users
    $sql = "SELECT * FROM chat_messages WHERE user_id IN (1, 2) ORDER BY timestamp ASC";
    $result = $conn->query($sql);

    $messages = array();
    while ($row = $result->fetch_assoc()) {
        $messages[] = $row;
    }

    echo json_encode($messages);
} else {
    echo json_encode(array("error" => "Invalid user ID"));
}

$conn->close();
?>
