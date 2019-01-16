Vue.component('movie-box', {
	props: ['movie'],
	template: `
		<div class="col-md-3 col-sm-6 movie-box-container">
			<div class="movie-box">
				<el-tooltip v-if=movie placement="top">
	  				<div slot="content" v-if=movie>{{movie.title}} ({{movie.year}})<br/>{{movie.genre}}<br />IMDB: {{movie.imdb_rating}}</div>
					<a :href=movie.imdb_url target="_blank" >
						<img :src=movie.poster class="movie-poster" />
					</a>
				</el-tooltip>
			</div>
		</div>
	`
})

new Vue({
  el: '#app',
  data: {
    title_search_movies: [],
    title_search: '',
    timeout:  null,
    selected_movies: [],
    suggested_movies: []
  },
  methods: {
	  loadAll() {
	    return [];
	  },
	  querySearchAsync(queryString, cb) {
	    axios.get('http://localhost:8000/_autocomplete?q=' + this.title_search).then(res => {
	    	data = JSON.parse(res.data.data)
	    	for(i=0; i < data.length; i++){
	    		data[i]['full_title'] = data[i]['title'] + ' (' + data[i]['year'] + ')'
	    	}
	    	this.title_search_movies = data
	    })

	    clearTimeout(this.timeout);
        this.timeout = setTimeout(() => {
          cb(this.title_search_movies);
        }, 1000 * Math.random());
	  },
	  createFilter(queryString) {
	    return (link) => {
	      return (link.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
	    };
	  },
	  handleSelect(item) {
	    this.selected_movies.push(item)
	    this.title_search = ''
	  },
	  fetch_predictions(event){
	  	movies = this.selected_movies
	  	if(movies.length > 0){
	  		req = "http://localhost:8000/_predict?movie_id="
	  		for(var i=0; i < movies.length; i++){
	  			req += String(movies[i].movie_id)
	  			if(movies.length - i > 1){
	  				req += "&movie_id="
	  			}
	  		} 
	  		//fetch predictions
	  		axios.get(req).then(res => this.suggested_movies = JSON.parse(res.data.data))
	  	}
	  }
	},
	 mounted() {
      this.links = this.loadAll();
    }
})
