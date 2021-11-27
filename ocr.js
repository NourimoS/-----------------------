const { spawn } = require("child_process");
const input = ".\\009.jpeg";
const output = ".\\009";
const lang = "ara_best+script/Arabic";
const tesseract = spawn("tesseract", [input, output, `-l ${lang}`]);

tesseract.on("close", (code) =>
	console.log(`child process closed with code ${code}`)
);

tesseract.stdout.on("data", (data) => {
	console.log(data);
});
tesseract.stderr.on("error", (data) => {
	console.log(data);
});
