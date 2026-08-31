import { spawn } from "node:child_process";

const forwarded = process.argv.slice(2);
const nextArgs = ["dev"];

for (let index = 0; index < forwarded.length; index += 1) {
  const argument = forwarded[index];
  if (argument === "--host") {
    nextArgs.push("--hostname", forwarded[index + 1] ?? "0.0.0.0");
    index += 1;
  } else if (argument !== "--strictPort") {
    nextArgs.push(argument);
  }
}

const child = spawn(process.execPath, ["node_modules/next/dist/bin/next", ...nextArgs], {
  stdio: "inherit",
});

child.on("exit", code => process.exit(code ?? 1));
for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => child.kill(signal));
}
