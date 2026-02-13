package main

import (
	"fmt"
)

func main() {
	fmt.Println("Running Go Script")

	apiKey := "0acdc43cd60846c0b19195fa8995a3a6"
	fmt.Println(apiKey)

	// resp, err := http.Get("google.com")
	// if err != nil {
	// 	panic(err)
	// }
	// defer resp.Body.Close() // TODO: Look up what defer does

	// body, err := io.ReadAll(resp.Body)
	// if err != nil {
	// 	panic(err)
	// }

	// fmt.Println(string(body))
}
