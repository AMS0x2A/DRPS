package org.drps;

import java.io.*;

public class ThreadedReader implements Runnable {
    public ThreadedReader(BufferedReader in) {
        this.in = in;
    }

    public void run() {
        do {
            try {
                line = in.readLine();
            } catch (IOException e) {
                line = null;
            }
        } while (line == null);
    }

    public String readLine() {
        Thread thread = new Thread(this);
        thread.start();
        try {
            thread.join();
        } catch (InterruptedException e) {}
        return line;
    }

    private final BufferedReader in;
    private volatile String line;
}