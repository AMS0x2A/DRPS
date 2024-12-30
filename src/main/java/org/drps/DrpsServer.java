package org.drps;

import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

class UsersDB {
    public static void read() {
        try {
            BufferedReader reader = new BufferedReader(new FileReader(file));
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.equals("{") || line.equals("}")) { continue; }

                String[] kvPair = line.split(":");
                String cleanKey = kvPair[0].split("\"")[1] + ":" + kvPair[1].split("\"")[0];
                String cleanValue = kvPair[2].split("\"")[1];

                User user = User.dehash(cleanValue);
                Database.put(cleanKey, user.username);
                Database.updateDB(cleanValue);
            }
            reader.close();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    public static void write() {
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter(file));

            StringBuilder data = new StringBuilder("{\n");
            int i = 0;
            int socks_len = Database.socks.size();
            for (String sock : Database.socks.keySet()) {
                String userHash = Database.getUserByKey(sock).hash();
                data.append(String.format("\"%s\":\"%s\"", sock, userHash));
                if (++i < socks_len) {
                    data.append(",\n");
                } else {
                    data.append("\n");
                }
            }
            data.append("}");

            writer.write(data.toString());
            writer.close();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    public static void clean() {
        try {
            FileWriter writer = new FileWriter(file);
            writer.write("");
            writer.close();
        } catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }

    private static File file = new File("/Users/ams/Desktop/CodingWorks/Java/DistributedRPS/DRPS/src/main/UsersDB.json");
}

class Worker extends Thread {
    Worker(Socket s) {
        sock = s;
        try {
            reader = new ThreadedReader(new BufferedReader(new InputStreamReader(sock.getInputStream())));
            writer = new ThreadedWriter(new PrintStream(sock.getOutputStream()));

            String key = s.getInetAddress().toString() + ":" + Integer.toString(s.getLocalPort());
            String username;
            if (!Database.socks.containsKey(key)) {
                writer.writeLine(DrpsMessage.REGISTER_USERNAME.toString());

                username = reader.readLine();
                while (Database.usernames.contains(username.toLowerCase())) {
                    writer.writeLine(DrpsMessage.USERNAME_TAKEN.toString());

                    username = reader.readLine();
                }
                user = new User(username);
                writer.writeLine(DrpsMessage.USERNAME_ACCEPTED.toString());
            } else {
                writer.writeLine(DrpsMessage.FOUND_USER.toString());

                String fromClient = reader.readLine();
                if (!fromClient.equals(DrpsMessage.ACK.toString())) {
                    System.err.println("Client (" + key + ") sent unexpected message: " + fromClient);
                }

                user = Database.getUserByKey(key);
                username = user.username;
                writer.writeLine(user.username);
            }
            Database.put(key, username);
            System.out.println(user.username + " connected to server");

            Database.commit();
        } catch (IOException ioe) {
            System.err.println(ioe);
        }
    }

    public void run() {
        try {
            try {
//                String username = Database.socks.get(
//                        sock.getInetAddress().toString() + ":" + Integer.toString(sock.getLocalPort())
//                );
                System.out.println(user.username + " thread running");

                while (true) {
                    String cmd = reader.readLine();
                    if (cmd.equals(DrpsMessage.DISCONNECT.toString())) { break; }
                    else if (cmd.equals(DrpsMessage.GET_STATS.toString())) {
                        printStats(user, writer);
                        continue;
                    }
                    printResult(RpsChoice.value(cmd), user, writer);
                }

                System.out.println(user.username + " disconnected. Thread stopping");
            } catch (NullPointerException npe) {
                System.err.println(npe);
                System.err.println("The client has disconnected");
            }
            Database.commit();
            sock.close();
        } catch (IOException ioe) {
            System.err.println(ioe);
        }
    }

    static void printStats(User user, ThreadedWriter writer) {
        try {
            writer.writeLine(user.toString());
        } catch (Exception ex) {
            writer.writeLine("Couldn't get stats");
        }
    }

    static void printResult(RpsChoice choice, User user, ThreadedWriter writer) {
        try {
            int result = Battle.print(choice, user, writer);
            Database.inc(user.username, result);
        } catch (Exception ex) {
            writer.writeLine("Failed in attempt to serve battle");
        }
    }

    Socket sock;
    User user;
    boolean inQueue = false;

    static ThreadedReader reader;
    static ThreadedWriter writer;
}

class Battle {
    public static void incTotalBattles(User user) {
        user.totalBattles++;
    }

    public static void incWins(User user) { user.wins++; }
    public static void incLoses(User user) { user.loses++; }

    public static int print(RpsChoice choice, User user, ThreadedWriter writer) {
        RpsChoice otherChoice = choice == RpsChoice.PAPER ? RpsChoice.SCISSORS : RpsChoice.ROCK;
        writer.writeLine(otherChoice.toString());

        int res = rps(choice, otherChoice);
        if (res == 0) { writer.writeLine("It's a draw"); }
        else if (res == 1) { writer.writeLine("You win"); }
        else { writer.writeLine("You lose"); }

        return res;
    }

    public static int rps(RpsChoice userChoice, RpsChoice otherChoice) {
        if (userChoice == otherChoice) { return 0; }

        switch (userChoice) {
            case RpsChoice.ROCK:
                switch (otherChoice) {
                    case RpsChoice.PAPER: return -1;
                    case RpsChoice.SCISSORS: return 1;
                }
                break;
            case RpsChoice.PAPER:
                switch (otherChoice) {
                    case RpsChoice.ROCK: return 1;
                    case RpsChoice.SCISSORS: return -1;
                }
                break;
            case RpsChoice.SCISSORS:
                switch (otherChoice) {
                    case RpsChoice.ROCK: return -1;
                    case RpsChoice.PAPER: return 1;
                }
                break;
        }
        return 0;
    }

    private static List<Object[]> battleQueue;  // [(Worker, RpsChoice)]
    private static final Random r = new Random();
}

class User {  // TODO: finish class equality
    public User(String username) {
        this.username = username;
        this.wins = 0;
        this.loses = 0;
        this.totalBattles = 0;
    }

    public String toString() {
        return "\tUsername: " + this.username + "\n" +
                "\tTotal Battles: " + this.totalBattles + "\n" +
                "\tWins: " + this.wins + "\tLoses: " + this.loses;
    }

    public String hash() {
        return String.format("%s,%d,%d,%d", username, totalBattles, wins, loses);
    }

    public static User dehash(String hash) {
        try {
            String[] fields = hash.split(",");
            if (fields.length != 4) { return null; }
            User user = new User(fields[0]);
            user.totalBattles = Integer.parseInt(fields[1]);
            user.wins = Integer.parseInt(fields[2]);
            user.loses = Integer.parseInt(fields[3]);
            return user;
        } catch (Exception e) { return null; }
    }

    public int hashCode() {
        return username.hashCode();
    }

    public boolean equals(Object o) {
        return (o instanceof User) && this.hashCode() == o.hashCode();
    }

    public String username;
    public int totalBattles;
    public int wins;
    public int loses;
}

class Database {
    public static void init() {
        db = new HashMap<String, User>();
        UsersDB.read();
    }
    public static boolean isMember(String username) { return db.containsKey(username.toLowerCase()); }
    public static boolean put(String key, String username) {
        if (isMember(username)) { return false; }
        socks.put(key, username);
        usernames.add(username.toLowerCase());
        db.put(username.toLowerCase(), new User(username));
        return true;
    }

    public static boolean put(String username) {
        if (isMember(username)) { return false; }
        usernames.add(username.toLowerCase());
        db.put(username.toLowerCase(), new User(username));
        return true;
    }

    public static User getUserByKey(String key) {
        if (!socks.containsKey(key)) {
            return null;
        }

        return getUser(socks.get(key));
    }

    public static User getUser(String username) {
        if (isMember(username)) { return db.get(username.toLowerCase()); }
        Database.put(username);
        return db.get(username);
    }

    public static void inc(String username, int result) {
        if (isMember(username)) {
            User user = Database.getUser(username);
            Battle.incTotalBattles(user);
            if (result == 1) { Battle.incWins(user); }
            else if (result == -1) { Battle.incLoses(user); }
        }
    }

    public static String updateDB(String userHash) {
        User user = User.dehash(userHash);
        if (user == null) { return null; }
        String username = user.username;
        if (!isMember(username)) { return null; }
        db.put(username.toLowerCase(), user);
        return username;
    }

    public static void commit() {
        UsersDB.write();
    }

    public static Map<String, User> getDb() { return Database.db; }

    public static void reset() {
        db.clear();
        socks.clear();
        usernames.clear();
    }

    private static Map<String, User> db;                        // username -> User
    public static Map<String, String> socks = new HashMap<>();  // sock -> username
    public static List<String> usernames = new ArrayList<>();   // [username]
}

public class DrpsServer {
    public static void main(String[] args) throws IOException {
        if (args.length < 1) {
            int q_len = 6;
            Socket sock;

            Database.init();

            ServerSocket servsock = new ServerSocket(Constants.port, q_len);

            System.out.println(
                "Disrtibuted RPS Server " + Constants.version + " starting up, listening at port " + Integer.toString(Constants.port) + "\n"
            );

            try {
                while (true) {
                    sock = servsock.accept();

                    new Worker(sock).start();
                }
            } catch (Exception e) {
                System.err.println("You broke it");
                e.printStackTrace();
            } finally {
                Database.reset();
                servsock.close();
            }
        }
//        } else if (args.length == 1 && (args[0].equals("--help") || args[0].equals("-h"))) {
//            usage();
//            System.exit(0);
        else {
            usage();
            System.exit(0);
        }
    }

    public static void usage() {
        System.out.println("Usage: ");
    }
}