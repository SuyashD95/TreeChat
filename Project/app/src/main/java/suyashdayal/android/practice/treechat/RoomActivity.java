package suyashdayal.android.practice.treechat;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class RoomActivity extends AppCompatActivity {

    private final String LOG_TAG = RoomActivity.class.getSimpleName();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_room);

        // Get the name of the room from the Intent that was received
        // to start {@link RoomActivity}
        String roomName = getIntent().getStringExtra("room_name");
        Log.i(LOG_TAG, "The name of the room is " + roomName);

        // Change the title of the {@link RoomActivity} to display the name of the room
        setTitle(roomName);

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