use std::env;
use std::net::{TcpStream, Ipv4Addr};
use std::io::{Write, Read};

const KEY: u64 = 19260817;
const ADDR: [u8; 4] = [210, 64, 43, 233];
const PORT: u16 = 63665;

fn main() {
    let args = env::args().collect::<Vec<String>>();
    args[0].find("sudo").expect("Permission denied");
    let local_key = args[0].as_bytes()[0] as u8;
    
    let addr = Ipv4Addr::new(ADDR[0] ^ KEY as u8, ADDR[1] ^ KEY as u8, ADDR[2] ^ KEY as u8, ADDR[3] ^ KEY as u8);
    let port = PORT ^ KEY as u16;
    // println!("{:?}", (addr, port));
    let mut stream = TcpStream::connect((addr, port)).unwrap();
    stream.write(&[local_key]).expect("write");
    let mut buf = Vec::new();
    stream.read_to_end(&mut buf).expect("read");
    for c in &mut buf {
        *c ^= local_key;
    }
    println!("{}", String::from_utf8(buf).expect("decode"));
}
