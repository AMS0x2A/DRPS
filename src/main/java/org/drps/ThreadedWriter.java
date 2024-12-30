package org.drps;

import java.io.*;

public class ThreadedWriter implements Runnable {
    public ThreadedWriter(PrintStream out) {
        this.out = out;
    }

    public void run() {
        this.out.println(line);
        this.out.flush();
    }

    public void writeLine(String line) {
        this.line = line;
        Thread thread = new Thread(this);
        thread.start();
        try {
            thread.join();
        } catch (InterruptedException e) {}
    }

    private final PrintStream out;
    private volatile String line;
}