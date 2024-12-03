package org.drps;

public enum RpsChoice implements ServerClientComms {
    ROCK, PAPER, SCISSORS;

    public static RpsChoice value(String s) {
        return switch (s.toUpperCase()) {
            case "ROCK" -> RpsChoice.ROCK;
            case "PAPER" -> RpsChoice.PAPER;
            case "SCISSORS" -> RpsChoice.SCISSORS;
            default -> null;
        };
    }
}