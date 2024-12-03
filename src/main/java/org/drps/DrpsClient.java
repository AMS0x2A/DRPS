package org.drps;

import java.io.*;
import java.net.*;

public class DrpsClient {
    public static void main(String[] args) {
        String serverName = null;

        if (args.length < 1) {
            serverName = "localhost";
        } else {
            usage();
            System.exit(0);
        }


        System.out.println("Distributed RPS Client " + Constants.version);
        System.out.println("Using server: " + serverName + ", Port: " + Constants.port);


        BufferedReader in = new BufferedReader(
                new InputStreamReader(System.in)
        );

        try {
            sock = new Socket(serverName, Constants.port);
            fromServer = new BufferedReader(new InputStreamReader(sock.getInputStream()));
            toServer = new PrintStream(sock.getOutputStream());

            String username = findUser(serverName);
            System.out.println("Welcome, " + username);
            System.out.println();

            String cmd;
            boolean cmd_is_quit;
            do {
                System.out.print(
                        "Rock\n" +
                        "Paper\n" +
                        "Scissors\n" +
                        "Stats\n" +
                        "Quit\n" +
                        ">> "
                );

                cmd = in.readLine();
                cmd_is_quit = cmd.toLowerCase().equals("quit");
                serveRequest(cmd, serverName);
            } while (!cmd_is_quit);
            System.out.println("Cancelled by user request");
            sock.close();
        } catch (IOException ioe) { System.out.println(ioe); }
    }

    static void serveRequest(String cmd, String serverName) {
        switch (cmd.toLowerCase()) {
            case "rock":
            case "paper":
            case "scissors":
                battle(RpsChoice.value(cmd), serverName);
                break;

            case "stats":
                printStats();
                break;

            case "quit":
                toServer.println(DrpsMessage.DISCONNECT.toString());
                toServer.flush();
                break;

            default:
                System.err.println("Invalid Choice");
        }
    }

    static void printStats() {
        try {
            toServer.println(DrpsMessage.GET_STATS.toString());
            toServer.flush();

            System.out.println(fromServer.readLine());
            System.out.println(fromServer.readLine());
            System.out.println(fromServer.readLine());
        } catch (IOException ioe) {
            System.err.println("Cannot get stats");
        }
    }

    static void battle(RpsChoice cmd, String serverName) {
        try {
            toServer.println(cmd.toString());  // send rps command
            toServer.flush();

            String otherChoice = fromServer.readLine();
            String response = fromServer.readLine();

            System.out.println("\tYou chose " + cmd.toString());
            System.out.println("\tThe other player chose " + otherChoice);
            System.out.println("\t" + response);
        } catch (IOException x) {
            System.err.println(x);
            System.err.println("Socket error");
        }
    }

    static String findUser(String serverName) {
        try {
            String msg = fromServer.readLine();
            String username = "";
            if (msg.equals(DrpsMessage.REGISTER_USERNAME.toString())) {
                BufferedReader in = new BufferedReader(
                    new InputStreamReader(System.in)
                );
                do {
                    System.out.print("Enter username: ");
                    username = in.readLine();
                    toServer.println(username);
                    toServer.flush();
                    msg = fromServer.readLine();
                } while (msg.equals(DrpsMessage.USERNAME_TAKEN.toString()));
            } else if (msg.equals(DrpsMessage.FOUND_USER.toString())) {
                toServer.println(DrpsMessage.ACK.toString());
                toServer.flush();
                username = fromServer.readLine();
            } else {
                System.err.println("Server sent unexpected message: " + msg);
            }
            return username;
        } catch (IOException ioe) {
            System.err.println("Socket error.");
        }
        return "Client/Server Comm Error";
    }

    static void usage() {
        System.out.println("Usage: ");
    }

    static Socket sock;
    static BufferedReader fromServer;
    static PrintStream toServer;
}