web3 = require("web3");

for (let i = 0; i < 255; i++) {
    // 0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365
    if (web3.utils.soliditySha3('' + i) == "0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365") {
        console.log(`Found = ${i}`);
        break;
    }
}
