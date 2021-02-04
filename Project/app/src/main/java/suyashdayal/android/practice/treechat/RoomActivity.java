package suyashdayal.android.practice.treechat;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;

public class RoomActivity extends AppCompatActivity {

    private final String LOG_TAG = RoomActivity.class.getSimpleName();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_room);

        // Get the name of the room from the Intent that was received
        // to start {@link RoomActivity}
        String roomName = getIntent().getStringExtra("room_name");
        // Change the title of the {@link RoomActivity} to display the name of the room
        setTitle(roomName);

        ArrayList<String> members = new ArrayList<>();
        members.add("Member 1  (Admin)");
        members.add("Member 2");
        members.add("Member 3");

        ArrayList<String> messages = new ArrayList<>();
        messages.add("This is the 1st message.");
        messages.add("This is the 2nd message.");
        messages.add("This is the 3rd message.");
        messages.add("This is the 4th message.");
        messages.add("This is the 5th message.");
        messages.add("This is the 6th message.");
        messages.add("This is the 7th message.");
        messages.add("This is the 8th message.");
        messages.add("This is the 9th message.");
        messages.add("This is the 10th message.");

        // Reference to the list of members participating in a given Room.
        ListView membersList = findViewById(R.id.member_list);
        // Reference to the list of messages exchanged in a given Room.
        ListView messageList = findViewById(R.id.message_list);

        // Setup a simple ArrayAdapter for demonstration purposes.
        ArrayAdapter<String> memberArrayAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_list_item_1, members);
        // Setup a simple ArrayAdapter for demonstration purposes.
        ArrayAdapter<String> messageArrayAdapter = new ArrayAdapter<>(this,
                android.R.layout.simple_list_item_1, messages);

        // Attach an adapter to retrieve the data source and inflate
        // the items on the list
        membersList.setAdapter(memberArrayAdapter);
        // Attach an adapter to retrieve the data source and inflate
        // the items on the list
        messageList.setAdapter(messageArrayAdapter);

        // Field to write a new message
        final EditText messageEditText = findViewById(R.id.create_room_field);

        // The button to broadcast the message to the Room
        Button sendMessageBtn = findViewById(R.id.create_room_button);
        // Attach a click listener for testing purposes
        sendMessageBtn.setOnClickListener((View v) -> {
            String message = messageEditText.getText().toString();

            if (TextUtils.isEmpty(message)) {
                Toast.makeText(RoomActivity.this, "Cannot send a blank message", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(RoomActivity.this, message, Toast.LENGTH_SHORT).show();
            }
        });
    }
}