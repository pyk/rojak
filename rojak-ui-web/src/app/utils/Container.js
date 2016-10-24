import React from 'react'
import { push } from 'redux-router'
import Navbar from './Navbar'
import { setKeyword, setScreenExpanded } from '../root/actions'
import { connect } from 'react-redux'

class Container extends React.Component {
    static propTypes = {
        children: React.PropTypes.any,
        root: React.PropTypes.object.isRequired,
        router: React.PropTypes.object.isRequired,
        setScreenExpanded: React.PropTypes.func.isRequired,
        setKeyword: React.PropTypes.func.isRequired,
        push: React.PropTypes.func.isRequired
    }

    componentDidMount () {
        const { router, setKeyword } = this.props
        if (router.params.keyword) {
            setKeyword(this.props.params.keyword)
        }
    }

    componentWillReceiveProps (nextProps) {
        const { root, router, setKeyword } = this.props
        if (root.keyword !== nextProps.root.keyword) {
            this.checkExpandedState(nextProps.root.keyword)
            this.updateRoute(nextProps.root.keyword)
        }

        if (nextProps.router.params.keyword !== router.params.keyword) {
            setKeyword(nextProps.router.params.keyword || '')
        }
    }

    checkExpandedState (keyword) {
        const { setScreenExpanded } = this.props
        setScreenExpanded(!!keyword.trim())
    }

    updateRoute (keyword) {
        const { push } = this.props
        let pathname = `/search/${keyword}`
        // if keyword is empty, change route to home
        if (keyword.trim().length === 0) {
            pathname = ''
        }
        push(pathname)
    }

    render () {
        const { root, children } = this.props
        const expandedClass = root.expanded ? 'expanded' : ''
        return (
          <div id="container" className={`rojakContainer ${expandedClass}`}>
              <NavbarWrapper expanded={root.expanded} />
              {children}
          </div>
        )
    }
}

function NavbarWrapper ({ expanded }) {
    if (expanded) return null
    return <Navbar />
}

export default connect(({ root, router }) => ({ root, router }), { setScreenExpanded, setKeyword, push })(Container)
