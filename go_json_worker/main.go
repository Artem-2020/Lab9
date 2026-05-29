package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"math"
	"os"
)

type Request struct {
	User      string    `json:"user"`
	Operation string    `json:"operation"`
	Numbers   []float64 `json:"numbers"`
}

type Response struct {
	Message     string  `json:"message"`
	Operation   string  `json:"operation"`
	Result      float64 `json:"result"`
	ProcessedBy string  `json:"processed_by"`
	Error       string  `json:"error,omitempty"`
}

type Job struct {
	Request  Request
	Response chan Response
}

func worker(jobs <-chan Job) {
	for job := range jobs {
		result, err := calculate(job.Request)
		response := Response{
			Message:     "Данные успешно обработаны в Go",
			Operation:   job.Request.Operation,
			Result:      result,
			ProcessedBy: "background goroutine",
		}

		if err != nil {
			response.Message = "Ошибка обработки данных"
			response.Error = err.Error()
		}

		job.Response <- response
	}
}

func calculate(request Request) (float64, error) {
	if len(request.Numbers) == 0 {
		return 0, errors.New("список numbers не должен быть пустым")
	}

	switch request.Operation {
	case "sum":
		return sum(request.Numbers), nil
	case "average":
		return sum(request.Numbers) / float64(len(request.Numbers)), nil
	case "max":
		return max(request.Numbers), nil
	default:
		return 0, fmt.Errorf("неизвестная операция: %s", request.Operation)
	}
}

func sum(numbers []float64) float64 {
	total := 0.0
	for _, number := range numbers {
		total += number
	}
	return total
}

func max(numbers []float64) float64 {
	result := math.Inf(-1)
	for _, number := range numbers {
		if number > result {
			result = number
		}
	}
	return result
}

func main() {
	var request Request
	if err := json.NewDecoder(os.Stdin).Decode(&request); err != nil {
		writeResponse(Response{
			Message: "Ошибка чтения JSON",
			Error:   err.Error(),
		})
		os.Exit(1)
	}

	jobs := make(chan Job)
	go worker(jobs)

	responseChannel := make(chan Response)
	jobs <- Job{
		Request:  request,
		Response: responseChannel,
	}

	writeResponse(<-responseChannel)
	close(jobs)
}

func writeResponse(response Response) {
	if err := json.NewEncoder(os.Stdout).Encode(response); err != nil {
		fmt.Fprintln(os.Stderr, err)
	}
}

