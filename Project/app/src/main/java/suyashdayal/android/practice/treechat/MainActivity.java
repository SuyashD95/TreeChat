package suyashdayal.android.practice.treechat;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    /** Button to let users sign in using their Google's account */
    TextView mGoogleLoginBtn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mGoogleLoginBtn = findViewById(R.id.google_login_btn);
        mGoogleLoginBtn.setOnClickListener(this);
    }

    /**
     * Called when the button to let users sign in into the application, using
     * Google's sign in functionality, has been clicked.
     *
     * @param v The view that was clicked.
     */
    @Override
    public void onClick(View v) {
        Toast.makeText(this, "Login with Google", Toast.LENGTH_SHORT).show();
    }
}