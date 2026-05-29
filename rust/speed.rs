#[no_mangle]
pub extern "C" fn rust_count_primes(limit: u32) -> u32 {
    let mut count = 0;
    let mut number = 2;

    while number <= limit {
        if is_prime(number) {
            count += 1;
        }
        number += 1;
    }

    count
}

fn is_prime(number: u32) -> bool {
    if number < 2 {
        return false;
    }

    if number == 2 {
        return true;
    }

    if number % 2 == 0 {
        return false;
    }

    let mut divisor = 3;
    while divisor * divisor <= number {
        if number % divisor == 0 {
            return false;
        }
        divisor += 2;
    }

    true
}

