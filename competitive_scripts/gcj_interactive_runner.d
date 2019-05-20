#!/usr/bin/env rdmd

import std.stdio, std.algorithm, std.range, std.concurrency, std.process, std.exception, std.string, std.conv;

string red(string s) {
    return "\x1B[31m" ~ s ~ "\x1B[0m";
}

string green(string s) {
    return "\x1B[32m" ~ s ~ "\x1B[0m";
}

string blue(string s) {
    return "\x1B[34m" ~ s ~ "\x1B[0m";
}


__gshared Tid printerTid;
__gshared ProcessPipes judge, your;

void teeReader(string inFile)(string prefix) {
    while (true) {        
        string s = mixin(inFile).readln;
        if (s == "") break;
        s = s.strip();
        send(printerTid, prefix ~ s);
    }
    mixin(inFile).close;
}

auto teePipe(string inFile, string outFile)(string prefix) {
    while (true) {
        string s = mixin(inFile).readln;
        if (s == "") break;
        s = s.strip;
        send(printerTid, prefix ~ s);
        mixin(outFile).writeln(s);
        mixin(outFile).flush;
    }
    mixin(inFile).close;
    mixin(outFile).close;
};

int main(string[] args) {
    enforce(args.count("--") == 1, "./interactive_runner.d judge -- your");
    auto judgeArgs = args.findSplitBefore(only("--"))[0].array[1..$];
    auto yourArgs = args.findSplitAfter(only("--"))[1].array;

    printerTid = spawn((){
        bool ended = false;
        while (!ended) {
            receive(
                (string s) { writeln(s); },
                (bool) { ended = true; }
            );
        }
    });

    judge = pipeProcess(judgeArgs, Redirect.all);
    your = pipeProcess(yourArgs, Redirect.all);

    spawn(&teePipe!("your.stdout", "judge.stdin"), "[>]  ".green);
    spawn(&teePipe!("judge.stdout", "your.stdin"), " [<] ".red);
    spawn(&teeReader!("your.stderr"), "[E]  ".green);
    spawn(&teeReader!("judge.stderr"), " [E] ".red);

    send(printerTid, text("[!] ".blue, "End your Process : ", wait(your.pid)));
    send(printerTid, text("[!] ".blue, "End judge Process : ", wait(judge.pid)));
    send(printerTid, true);
    return 0;
}
