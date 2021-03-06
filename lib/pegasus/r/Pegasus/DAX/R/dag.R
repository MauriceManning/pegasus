#' This job represents a sub-DAG that will be executed by the workflow
#'
#' @details
#' The name argument can be either a string, or a \code{File} object. If
#' it is a \code{File} object, then this job will inherit its name from the
#' \code{File} and the \code{File} will be added in a \code{<uses>} with \code{transfer=TRUE},
#' \code{register=FALSE}, and \code{link=input}.
#'
#' @examples
#' dagjob1 <- DAG(file="foo.dag")
#' dagfile <- File("foo.dag")
#' dagjob2 <- DAG(dagfile)
#'
#' @param file The logical name of the DAG file, or the DAG File object
#' @param id The ID of the DAG job [default: autogenerated]
#' @param node.label The label for this job to use in graphing
#' @return The sub-DAG job
#' @export
DAG <- function(file, id=NULL, node.label=NULL) {

  if (class(file) == "File") {
    file <- file
  } else if (is.character(file)) { # TODO: verify unicode
    file <- File(name=file)
  } else {
    stop(paste("Invalid file:", file))
  }
  abstract.job <- AbstractJob(id=id, node.label=node.label)

  object <- list(abstract.job=abstract.job, file=file)
  class(object) <- "DAG"
  return(object)
}

Unicode.DAG <- function(dag) {
  return(paste("<DAG ", dag$abstract.job$id, " ", dag$file$catalog.type$name, ">", sep=""))
}

ToXML.DAG <- function(dag) {
  e <- Element('dag', list(
    id=dag$abstract.job$id,
    file=dag$file$catalog.type$name,
    `node-label`=dag$abstract.job$node.label
  ))
  e <- InnerXML(dag$abstract.job, e)
  return(e)
}

# ###############################
# Add-in functions for R
# ###############################

Equals.DAG <- function(dag, other) {
  if (class(other) == "DAG") {
    if (!Equals(dag$file, other$file)) {
      return(FALSE)
    }
    return(Equals(dag$abstract.job, dag$abstract.job))
  }
  return(FALSE)
}

#' @rdname AddProfile
#' @method AddProfile DAG
#' @seealso \code{\link{DAG}}
#' @export
AddProfile.DAG <- function(obj, profile) {
  obj$abstract.job$profile.mixin <- AddProfileMixin(obj$abstract.job$profile.mixin, profile)
  return(obj)
}

#' @rdname AddInvoke
#' @method AddInvoke DAG
#' @seealso \code{\link{DAG}}
#' @export
AddInvoke.DAG <- function(obj, invoke) {
  obj$abstract.job$invoke.mixin <- AddInvokeMixin(obj$abstract.job$invoke.mixin, invoke)
  return(obj)
}
