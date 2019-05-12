#!/usr/bin/env rdmd
import std.stdio, std.process, std.path;

void main(string[] args) {
    if (args.length < 3) {
        writeln("usage : dhelper.d filename.d (b|t|s|sn)");
        return;
    }
    string source = args[1];
    string command = args[2];
    string sourceName = source.stripExtension;    
    final switch (command) {
    case "b":
        string[] list;
        list ~= ["dub", "build", "--skip-registry=all"];
        list ~= ["--single", source];
        list ~= args[3..$];
        spawnProcess(list).wait;
        break;
    case "r":
        string[] list;
        list ~= ["dub", "build", "--skip-registry=all"];
        list ~= ["--single", source];
        list ~= args[3..$];
        spawnProcess(list).wait;
        spawnProcess(["./" ~ sourceName]);
        break;
    case "t":
        string[] list;
        list ~= ["dub", "build", "--skip-registry=all"];
        list ~= ["--single", source];
        list ~= args[3..$];
        spawnProcess(list).wait;
        spawnProcess(["judge.py", "-n", sourceName]).wait;
        break;
    case "s":
        string[] list;
        list ~= ["dub", "run", "dunkelheit:combine", "--"];
        list ~= ["-i="~source, "-o="~sourceName~"_submit.d"];
        list ~= ["-c", "-u"];
        spawnProcess(list).wait;
        break;
    case "sn":
        string[] list;
        list ~= ["dub", "run", "dunkelheit:combine", "--"];
        list ~= ["-i="~source, "-o="~sourceName~"_submit.d"];
        spawnProcess(list).wait;
        break;
    }
}
