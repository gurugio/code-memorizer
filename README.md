# code-memorizer

Code Memorizer: help you to memorize code

This program replaces some code lines to the blank comment lines.
If you have such a good example source code that you really want to memorize it,
you can remove some lines of the example source with this program and fill out the blank lines.
First try level 1 (replace only one line) and then try higher levels.
(This program removes only real source code, not comment or too short line)

positional arguments:
  filename              file to memorize

optional arguments:
  -h, --help            show this help message and exit
  -l LEVEL, --level LEVEL
                        how many lines to be commented
  -p PREFIX, --prefix PREFIX
                        string with which comment starts
  -o OUTPUT, --output OUTPUT
                        do not replace source file and write result to another file

## Example

try with the "guessing game code" from https://doc.rust-lang.org/book/ch02-00-guessing-game-tutorial.html
```
$ python codememory.py -l 3 -p "#" -o out.ex.rs ex.rs
INFO:root:write output file=out.ex.rs
$ cat out.ex.rs
use rand::Rng; // codememory:skip
use std::cmp::Ordering; // codememory:skip
use std::io; // codememory:skip

fn main() {
    println!("Guess the number!");

    let secret_number = rand::thread_rng().gen_range(1..=100);

    loop {
# ADD CODE HERE!!!!!!!!!!!!!!!!!

# ADD CODE HERE!!!!!!!!!!!!!!!!!

        io::stdin()
            .read_line(&mut guess)
            .expect("Failed to read line");

        let guess: u32 = match guess.trim().parse() {
            Ok(num) => num,
            Err(_) => continue,
        };

        println!("You guessed: {guess}");

        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small!"),
# ADD CODE HERE!!!!!!!!!!!!!!!!!
            Ordering::Equal => {
                println!("You win!");
                break;
            }
        }
    }
}
```
