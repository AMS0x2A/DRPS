package org.drps;

public enum DrpsMessage implements ServerClientComms {
    TEST, INIT,
    ACK, HANDSHAKE,
    ACKACK, HEADNOD,

    GET_STATS,

    REGISTER_USERNAME, USERNAME_TAKEN, FOUND_USER,
    USERNAME_ACCEPTED,

    DISCONNECT;

    public static DrpsMessage value(String s) {
        return switch (s.toUpperCase()) {
            case "TEST" -> DrpsMessage.TEST;
            case "INIT" -> DrpsMessage.INIT;
            case "ACK" -> DrpsMessage.ACK;
            case "HANDSHAKE" -> DrpsMessage.HANDSHAKE;
            case "ACKACK" -> DrpsMessage.ACKACK;
            case "HEADNOD" -> DrpsMessage.HEADNOD;
            case "GET_STATS" -> DrpsMessage.GET_STATS;
            case "REGISTER_USERNAME" -> DrpsMessage.REGISTER_USERNAME;
            case "USERNAME_TAKEN" -> DrpsMessage.USERNAME_TAKEN;
            case "FOUND_USER" -> DrpsMessage.FOUND_USER;
            case "USERNAME_ACCEPTED" -> DrpsMessage.USERNAME_ACCEPTED;
            case "DISCONNECT" -> DrpsMessage.DISCONNECT;
            default -> null;
        };
    }

}