import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';
import { BACKEND_URL } from '../constants';

class QuestionView extends Component {
  constructor(props){
    super(props);
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: null,
    }
  }

  componentDidMount() {
    this.getCategories();
    this.getQuestions();
  }

  getCategories = () => {
    $.ajax({
      url: `${BACKEND_URL}/categories`,
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
      }
    })
  };

  getQuestions = () => {
    $.ajax({
      url: `${BACKEND_URL}/questions?page=${this.state.page}`,
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: null })
      },
      error: () => {
        alert('Unable to load questions. Please try your request again')
      }
    })
  };

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory= (id) => {
    $.ajax({
      url: `${BACKEND_URL}/categories/${id}/questions`,
      type: "GET",
      success: (result) => {
        console.log(result.questions);
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: id })
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
      }
    })
  };

  submitSearch = (searchTerm) => {
    console.log(searchTerm);
    $.ajax({
      url: `${BACKEND_URL}/questions?query=${searchTerm}`,
      type: "GET",
      success: (result) => {
        console.log(result.questions);
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions})
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
      }
    })
  };

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `${BACKEND_URL}/questions/${id}`,
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
          }
        })
      }
    }
  };

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
            {this.state.categories.map((category) => (
              <li key={category.id} onClick={() => {this.getByCategory(category.id)}}>
                {category.type}
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default QuestionView;
