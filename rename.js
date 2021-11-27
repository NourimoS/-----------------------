const { rename, readdirSync } = require("fs");
const files = readdirSync("./").filter((v) => v.endsWith(".jpeg"));
files.forEach((old) => {
	const newName = old.split(".")[0].padStart(3, "0");
	rename(old, `${newName}.jpeg`, (err) => {
		if (err) throw err;
		console.log(`fileName changed form ${old} =>${newName}`);
	});
});
