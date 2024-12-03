package org.drps;

import java.io.*;
import java.net.*;

// Press Shift twice to open the Search Everywhere dialog and type `show whitespaces`,
// then press Enter. You can now see whitespace characters in your code.
public class Main {
    public static void main(String[] args) throws IOException {
        if (args.length > 0 && args[0].toLowerCase().equals("-s")) {
            DrpsServer.main(new String[] { });
        } else {
            DrpsClient.main(new String[] { });
        }
    }
}