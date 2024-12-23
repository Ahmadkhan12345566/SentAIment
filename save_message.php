<?php
header("Access-Control-Allow-Origin: *"); // Allow all origins
header("Access-Control-Allow-Methods: POST, OPTIONS"); // Allow methods
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

// Retrieve and decode JSON input data
$input = json_decode(file_get_contents('php://input'), true);

// Extract and sanitize input data
$user_id = isset($input['user_id']) ? intval($input['user_id']) : 0;
$message = isset($input['message']) ? trim($input['message']) : '';
$sentiment_score = isset($input['sentiment_score']) ? floatval($input['sentiment_score']) : 0.0;

if ($user_id > 0 && !empty($message)) {
    // Prepare SQL query
    $sql = "INSERT INTO chat_messages (user_id, message, sentiment_score) VALUES (?, ?, ?)";
    $stmt = $conn->prepare($sql);

    if ($stmt) {
        $stmt->bind_param("isd", $user_id, $message, $sentiment_score);

        if ($stmt->execute()) {
            echo json_encode(array("success" => "Message saved successfully"));
        } else {
            echo json_encode(array("error" => "Error executing query: " . $stmt->error));
        }

        $stmt->close();
    } else {
        echo json_encode(array("error" => "Error preparing statement: " . $conn->error));
    }
} else {
    echo json_encode(array("error" => "Invalid input data"));
}

$conn->close();
?>
