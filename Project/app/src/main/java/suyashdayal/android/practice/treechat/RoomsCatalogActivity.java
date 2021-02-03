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

public class RoomsCatalogActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_rooms_catalog);

        ArrayList<String> strings = new ArrayList<>();
        strings.add("Room 1");
        strings.add("Room 2");
        strings.add("Room 3");
        strings.add("Room 4");
        strings.add("Room 5");

        // Setup a simple ArrayAdapter for demonstration purposes.
        ArrayAdapter<String> stringArrayAdapter = new ArrayAdapter<>(this, android.R.layout.simple_list_item_1, strings);

        // Field to enter the name of a new Room
        final EditText createRoomEditText = findViewById(R.id.create_room_field);

        // Reference to the List of Rooms displayed on the {@link RoomsCatalogActivity}.
        ListView roomsList = findViewById(R.id.rooms_list);
        roomsList.setAdapter(stringArrayAdapter);

        // The button to create a new Room
        Button createRoomBtn = findViewById(R.id.create_room_button);

        // Attach a click listener for testing purposes
        createRoomBtn.setOnClickListener((View v) -> {
            String newRoom = createRoomEditText.getText().toString();

            if (TextUtils.isEmpty(newRoom)) {
                Toast.makeText(RoomsCatalogActivity.this, "Enter the Room name", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(RoomsCatalogActivity.this, newRoom + " is created", Toast.LENGTH_SHORT).show();
            }
        });
    }
}